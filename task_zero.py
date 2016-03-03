import download_HTML_data as d
import populate_database as p

d.HTML_parse()
success = p.one_time_populate()
if success:
	print "DB created successfully"
exit()