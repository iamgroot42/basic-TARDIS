import requests
from pyparsing import oneOf, nums, alphas, restOfLine, alphanums, printables, empty
from pyparsing import Word, Optional, CharsNotIn, White, Group, SkipTo, Or

DATA_LINK = "http://kurucz.harvard.edu/atoms/1401/gf1401.gam"
FIRST_MAPPING = {}
SECOND_MAPPING = {}
GLOBAL_GRAMMAR = []
PARSED_DATA = []
COLUMNS = ["ELEM", "index(J)", "E(cm-1)", "J", "label", "g Lande'", "sum A", "C4", "C6", "sum f", "3 largest eigenvector components"]

def parse_mapping(data):
	'''
	Takes a list of strings and returns the (character,configuration) mapping in it
	The 'data' passed is actually the metadata at ths tartting of the file, which specifies
	characters which have to be replaced with configurations.
	For example, 'u sp 5d' indicates that u is to be replaced with 'sp 5d'
	The function uses the fact that different mappings are separated by a gap of at least two spaces.
	So, data is parsed to separate out individual mappings. Then, the part after the character is joined
	to create a mapping. 
	'''
	mapping = {}
	# Defined two grammars, as Optional() wasn't working as expected:
	map_parse1 = CharsNotIn(' ') + White() + Word(alphanums) + White(exact=1) + Word(alphanums) + White(min=2) + restOfLine
	map_parse2 = CharsNotIn(' ') + White() + Word(alphanums) + White(min=2) + restOfLine
	for row in data:
		row_copy = row
		while len(row_copy) > 0:
			# If it's a two-level confiugration:
			try:
				temp = map_parse1.parseString(row_copy)
				mapping[temp[0]] = ' '.join([temp[2],temp[4]])
				row_copy = temp[-1]
			except:
				# If it's a single-level configuration:
				try:
					temp = map_parse2.parseString(row_copy)
					mapping[temp[0]] = temp[2]
					row_copy = temp[-1]
				except:
					# Parsing error, so mappings must be complete
					return mapping


def parse_data():	
	'''
	Take the data which is to be parsed as input (a list of lines) and
	creates an SQL database for the same.
	'''
	# Try reading from a file to avoid unnecessary GET requests:
	try:
		f = open("gf1401.gam",'r')
		rawData = f.read()
	except:
		# File doesn't exist/ File I/O error
		try:
			print "Downloading file ..."
			r = requests.get(DATA_LINK)
			rawData = r.text
			f = open(DATA_LINK.split("/")[-1],'w')
			f.write(rawData)
			f.close()
		except:
			print "GET request failed : check Internet connection"
			return False

	global FIRST_MAPPING
	global SECOND_MAPPING
	global PARSED_DATA
	global GLOBAL_GRAMMAR

	rawData = rawData.splitlines()
	FIRST_MAPPING = parse_mapping(rawData[1:17])
	SECOND_MAPPING = parse_mapping(rawData[17:33])
	GLOBAL_GRAMMAR = grammar_list()
	mainData = rawData[38:] 
	for row in mainData:
		PARSED_DATA.append(parse_string(row))
	return True


def grammar_list():
	'''
	Returns a list of the grammars required to parse individual data entries in the given table.
	The grammars are as generic as possible. Thus, they should work for any file of the form gfxxyy.gam
	Explanation for grammars :
		- Scientific Number : (-)x.yE(+-)z, where the characters in brackets are optional, and 'x','y' and 'z' are
		    numbers. Scientific notation dictates that x be in [0,9], so it only one digit.Also, y must be at least
		    two digits long.
		- Bracket Config : Grammar for configurations which contain a bracket (like the second component of an 
			eigenvector in the last coulm of given data).
		- Elem : The first entry in the dataset ; is of the form (-)x.y[ODD,EVEN], where 'x' and 'y' are the atomic 
		    number and charge respectively
		- index(J) : a natural number.The optional '-' is added so that this grammar may be reused later.
		- E : A number of the form (-)x.y, where 'x' and 'y' are numbers, and the '-' is optional.
		- J : A number of the form x.y, where 'x' and 'y' are numbers.
		- Label : Rerpresents configuration. Extracted by taking away by other parts of the grammar, as defining a
		    grammar for it is quite tricky. Doing so also avoids any errors that may have occured because of changes in
		    the level's grammar.
		- G Lande' : same form as 'E'
		- Sum A : same form as 'Scientific Number'
		- C4 : same form as 'Scientific Number'
		- C6 : same form as 'Scientific Number'
		- Sum f : same form as 'E'
		- Single eigenvector commponents : of the form X Y Z, where X is the same form as 'E', Y is 
		   of the form 'BRACKET_CONFIG', and Z is a natural number. 
	'''
	grammars = []

	scientific_number = Group(Optional("-") + Word(nums,exact=1) + "." + Word(nums,min=2) + "E" + oneOf(["+","-"]) + Word(nums,min=2))
	ELEM = Group(Optional("-") + Word(alphanums + ".")) + White() + restOfLine
	INDEX = Word(nums) + White() + restOfLine
	E = Group(Optional("-") + Word(nums) + Optional("." + Word(nums))) + White()  + restOfLine
	J = Group(Word(nums) + "." + Word(nums)) + White() + restOfLine
	SUMA = scientific_number + Optional(White()) + restOfLine
	BRACKET_CONFIG = Group( CharsNotIn(' ',exact=1) + "(" + Word(alphanums) + ")" + Word(nums) + Word(alphas)) + Optional(White()) + restOfLine
	NATURAL_NUMBER = Word(nums) + Optional(White()) + restOfLine
	LABEL = SkipTo(J | SUMA) + restOfLine  # '| SUMA', as it can be of that form in second half of document

	grammars.append(ELEM)  # ELEM 
	grammars.append(INDEX)  # index(J) 
	grammars.append(E)  # E(cm-1) 
	grammars.append(J)  #J 
	grammars.append(LABEL)  #label
	grammars.append(J | SUMA)  # g'Lande (is same as E in terms of parsing). Can be of the form 'SUMA' for second half of document
	grammars.append(SUMA)  # SUM A
	grammars.append(SUMA) # C4 (is same as SUMA in terms of parsing)
	grammars.append(SUMA) # C6 (is same as SUMA in terms of parsing)
	grammars.append(E) # sum f (is same as E in terms of parsing)
	# 3 largest eigenvector components :
	# First eigenvector:
	grammars.append(ELEM)  # First componenet
	grammars.append(BRACKET_CONFIG)  # Second component
	grammars.append(NATURAL_NUMBER)  # Third component
	# Second eigenvector:
	grammars.append(ELEM)  # First componenet
	grammars.append(BRACKET_CONFIG)  # Second component
	grammars.append(NATURAL_NUMBER)  # Third component
	# Third eigenvector:
	grammars.append(ELEM)  # First componenet
	grammars.append(BRACKET_CONFIG)  # Second component
	grammars.append(NATURAL_NUMBER)  # Third component

	return grammars


def parse_string(test):
	'''
	Takes a string (representing a single row entry) and parses it according to the grammars specified glboally.
	Returns a list containing the parsed data (by columns)
	'''
	grammars = grammar_list()
	output = []

	for grammar in grammars:
		try:
			parsed = grammar.parseString(test)
			output.append(''.join(parsed[0]))
			test = parsed[-1]
		except:
			# Can't parse any more ; stop parsing
			break
	return output


def parse_final():
	'''
	Takes the parsed data( list of lists), and performs substitutions according to the mapping specified
	as the start of the file. Applies first mapping for first half of the document, and second mapping 
	for the second half.
	The substitutions are performed by trying to match every field with the grammar below, and making
	substitutions whenever the grammar's rule s satisfied.
	'''
	if not parse_data():
		return False

	global PARSED_DATA
	global FIRST_MAPPING
	global SECOND_MAPPING

	SUBS = CharsNotIn('(') + "(" + Word(alphanums) + ")" + restOfLine
	for row in PARSED_DATA:
		for i in range(len(row)):
			# First half of data ; first mapping will apply:
			if len(row)>6:
				try:
					parsed = SUBS.parseString(row[i])
					parsed[0] = FIRST_MAPPING[parsed[0]]
					row[i] = ''.join(parsed)
					# print parsed
				except:
					pass
			# Second half of data ; second mapping will apply:
			else:	
				try:
					parsed = SUBS.parseString(row[i])
					parsed[0] = SECOND_MAPPING[parsed[0]]
					row[i] = ''.join(parsed)
				except:
					pass
	return True
