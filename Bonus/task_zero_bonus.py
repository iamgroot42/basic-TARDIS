import parsing as p

print "Parsing..."
data = p.parse_final()

if data:
	print data
else:
	print "Parsing failed"
