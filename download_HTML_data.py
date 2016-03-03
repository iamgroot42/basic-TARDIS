import json
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

DATA_LINK = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&all=all&ascii=html"
FILE_NAME = "raw_data.html"

response = requests.get(DATA_LINK)

# To check if a string contains any digits:
def contains_digits(s):
    return any(char.isdigit() for char in s)

# Returns atomic symbol for passed isotope:
def atomic_symbol(raw_data,symbol):
	if (contains_digits(raw_data.text.strip()) is False) and ( raw_data.text.strip() != symbol ):
		return raw_data.text.strip()
	return symbol

# Takes HTML data (split by <td> tags) and creates a tuple, representing an element:
def data_to_row(raw_data,symbol,repeat=True):
	return_data = {}
	# Hydrogen's isotopes : special case:
	if repeat:
		if symbol not in ["H","D","T"]:
			offset = -2
		else:
			offset = -1
	else:
		offset = 0
	for i in range(len(raw_data)):
		raw_data[i] = raw_data[i].text.strip()
	# Necessary fields:
	return_data['Symbol'] = symbol
	return_data['Isotope'] = raw_data[offset+2]
	return_data['Relative Atomic Mass'] = raw_data[offset+3]
	# Optional fields:
	try:
		return_data['Isotopic Composition'] = raw_data[offset+4]
	except:
		return_data['Isotopic Composition'] = ''
	try:
		return_data['Standard Atomic Weight'] = raw_data[offset+5]
	except:
		return_data['Standard Atomic Weight'] = ''
	try:
		return_data['Notes'] = raw_data[offset+6]
	except:
		return_data['Notes'] = ''
	return return_data

# Write atomic-table to JSON file:
def write_to_json(file_name = FILE_NAME):
	try:
		html_file = open(file_name,'r')
		html_raw = html_file.read()
	except:
		print "File I/O Error"
		exit()
	d = pq(html_raw)
	D = d("tr")
	C = []
	for x in D:
		try:
			if "hr" in d(x).html():
				C.append([])
			else:
				C[len(C)-1].append(d(x).html())	
		except:
			continue
	# Hard-code ( for this website )
	C[0]=C[0][2:]
	C[-1]=C[-1][:1]
	# Main array to store itnermediate data:
	mainDB = []
	# Atomic number of element under consideration:
	a_no = 1 
	# Atomic symbol of eleelement under consideration:
	a_symbol = "H" 
	# Signifies whether an element is an isotope or not:
	repeated = False 
	# Iterating through raw HTML data:
	for elements in C:
		temp_group = {}
		temp_list = []
		# To check for atomic number (same for isotopes):
		repeated = False
		for isotopes in elements:
			soup = BeautifulSoup(isotopes)
			row = soup.find_all("td")
			# Special case (Hydrogen) :
			if a_no == 1:
				a_symbol = atomic_symbol(row[0],a_symbol)
			a_symbol = atomic_symbol(row[1],a_symbol)
			temp_group['Atomic Number'] = str(a_no)
			yolo = data_to_row(row,a_symbol,repeated)
			temp_list.append(yolo)
			repeated = True
		a_no += 1
		temp_group['Data'] = temp_list
		mainDB.append(temp_group)
	# Writing JSON object to file:
	with open('periodic_table.json', 'w') as outfile:
	    json.dump(mainDB, outfile)
	outfile.close()

# Download HTML page and parse it's content to JSON:
def HTML_parse(data_link = DATA_LINK,file_name = FILE_NAME):
	try:
		outfile = open(file_name, 'w')
		outfile.write(response.text)
		outfile.close()
	except:
		print "I/O Error"
	write_to_json(file_name)