# Silicon, charge 1 
# GFxxyy.GAM has all energy levels with the J, label, Lande g, sums of As, 
# C4s, C6s, and the 3 largest eigenvector components.

import requests
from pyparsing import oneOf, nums, alphas, restOfLine, alphanums
from pyparsing import Word, Optional, CharsNotIn, White, Group

OLE = "14.01"
# DATA_LINK = "http://kurucz.harvard.edu/atoms/1401/gf1401.gam"
# r = requests.get(DATA_LINK)
# raw_data = r.text

f = open("gf1401.gam.txt",'r')
raw_data = f.read()
lel = raw_data.splitlines()



# scientific_number = Optional("-") + Word(nums,exact=1) + "." + Word(nums,min=2) + "E" + oneOf(["+","-"]) + Word(nums,min=2)

# Scientific Floating Numbers:
# test = ["4.22E+11","0.00E+00","1.19E+08","7.47E-33","-8.65E-14","1.60418000000000E+05","-1.64168325628021E+05"]

column_headers = lel[37]
# main_data = lel[38:]
# for x in test:
# 	try:
# 		print scientific_number.parseString(x,"parseAll")  # 'parseAll' is optional
# 	except ParseException, err:
# 		print "Couldn't parse"

# First column:
# elem = OLE + oneOf(["EVE","ODD"])

# Second column:
# index = Word(nums)

# Third column:
# test = ["-175445.269","150442.500"]
# e = Optional("-") + Word(nums) + Optional("." + Word(nums))
# for x in test:
# 	try:
# 		print e.parseString(x,"parseAll")  # 'parseAll' is optional
# 	except ParseException, err:
# 		print "Couldn't parse"

# Fourth column:
# j = Word(nums) + "." + Word(nums)

# Not required : [1,2,3,4,5,6]

# Just using 'split':
# example = lel[38]
# example = example.split(' ',1)
# print "Label : ",example[0]
# example = example[1].strip()
# example = example.split(' ',1)
# print "Index(J) : ",example[0]
# example = example[1].strip()
# example = example.split(' ',1)
# print "E : ",example[0]
# example = example[1].strip()
# print example

grammars = []
output = []
row = lel[38]

scientific_number = Group(Optional("-") + Word(nums,exact=1) + "." + Word(nums,min=2) + "E" + oneOf(["+","-"]) + Word(nums,min=2))

ELEM = Optional("-") + Word(alphanums + ".") + White() + restOfLine
grammars.append(ELEM)
INDEX = Word(nums) + White() + restOfLine
grammars.append(INDEX)
E = Group(Optional("-") + Word(nums) + Optional("." + Word(nums))) + White()  + restOfLine
grammars.append(E)
J = Group(Word(nums) + "." + Word(nums)) + White() + restOfLine
grammars.append(J)
# label : the real deal

grammars.append(J)  # g'Lande is same as E in terms of parsing
SUMA = scientific_number + Optional(White()) + restOfLine
grammars.append(SUMA) 
grammars.append(SUMA) #C4 is same as SUMA in terms of parsing
grammars.append(SUMA) #C6 is same as SUMA in terms of parsing
grammars.append(E) #sumf is same as E in terms of parsing

for grammar in grammars:
	parsed = grammar.parseString(row)
	output.append(''.join(parsed[0]))
	row = parsed[-1]

print output