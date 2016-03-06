import parsing as p

success = p.parse_final()

if success:
	print p.PARSED_DATA
else:
	print "Parsing failed"