import download_HTML_data as d
import populate_database as p

def zero_task():
	'''
	Parse data from HTML into .json, and then use that .json file to populate database
	'''
	d.HTML_parse()
	success = p.one_time_populate()
	if success:
		print "DB created successfully"


zero_task()
