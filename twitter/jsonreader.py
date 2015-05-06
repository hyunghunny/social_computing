##
# JSON file reader
# @author webofthink@snu.ac.kr
#
import json

##
# read JSON file
# @param file_name JSON file name
# @return JSON data
#
def read(file_name):
	with open(file_name) as json_file:
		json_data = json.load(json_file)
	return json_data

# Simple test
#json_objs = read('tweets.json')
#print (json_objs)