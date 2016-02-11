#!/usr/bin/env python

import argparse, json, urllib2

parser = argparse.ArgumentParser(description="script for improving DRMC report data")
parser.add_argument('-i', '--input', type=str, required=True, help='source data file.')
args = parser.parse_args()

data_source = args.input
apifileHandle = open('./auth/api_url', 'r')
for line in apifileHandle:
	api_url = line
apifileHandle.close()


fileHandle = open(data_source, 'r')
counter = 0
for line in fileHandle:
	fields = line.split('|')
	bytes = fields[0]
	path = fields[1]

	# print("checking: "+path), # prints path
	path_parts = path.split('---')
	if len(path_parts) == 4:
		path_artist = path_parts[0]
		path_title = path_parts[1]
		path_objectnumber = path_parts[2]
		path_objectid = path_parts[3]
		req = json.load(urllib2.urlopen(api_url+path_objectid))
		tms_lastname_firstname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
		tms_title = req["GetTombstoneDataRestIdResult"]["Title"]
		tms_object_number = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
		tms_objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
		tms = u"Artist: {}\nTitle: {}\nObject Number: {}\nObjectID: {}".format(tms_lastname_firstname, tms_title, tms_object_number, tms_objectid)
		# print tms

		extract_name = path_artist.split('/')
		cleaned_name = extract_name[2].replace('_',' ')

		cleaned_objectnumber = path_objectnumber.replace('_','.')

		if cleaned_objectnumber != tms_object_number:
			counter += 1
			print "mismatch number "+str(counter)+": "+ path,
			print "Given ObjectID refers to the following work in CEMS"
			print tms+"\n"
			

		# print cleaned_name
		# print tms_lastname_firstname
print counter


fileHandle.close()