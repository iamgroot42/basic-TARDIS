from pyparsing import Word, Literal, alphas, ParseException, Combine, Optional, nums, CaselessLiteral
import requests

# DATA_LINK = "http://kurucz.harvard.edu/atoms/1401/gf1401.gam"
# r = requests.get(DATA_LINK)
# raw_data = r.text

f = open("gf1401.gam.txt",'r')
raw_data = f.read()
lel = raw_data.split('\n')

integer = Optional(Word("+-")) + Word(nums)
power = CaselessLiteral("E") + integer
after_decimal = Literal(".") + Word(nums)
floatnumber = ( integer ) | 
			  ( integer + Optional( after_decimal) + Optional( power )
# try:
# print integer.parseString("-00")
print floatnumber.parseString("-14.-6")
# except ParseException, err:
	# print "Couldn't parse"


lel[0] 