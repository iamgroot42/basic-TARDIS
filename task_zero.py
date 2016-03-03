import populate_database as p
import download_HTML_data as d

d.HTML_parse()
success = p.one_time_populate()
if success:
	print "DB created successfully"
exit()