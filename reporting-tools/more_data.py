#!/usr/bin/env python

import argparse, json, urllib2, csv, unicodedata

parser = argparse.ArgumentParser(description="script for improving DRMC report data")
parser.add_argument('-i', '--input', type=str, required=True, help='source data file.')
parser.add_argument('-o', '--output', type=str, required=True, help='where to put csv')
args = parser.parse_args()

data_source = args.input
apifileHandle = open('./auth/api_url', 'r')
for line in apifileHandle:
	api_url = line
apifileHandle.close()

csv_path = args.output
c = csv.writer(open(csv_path, "wb"))
c.writerow(["bytes","Title","Artist","Object Number","Object ID","Department","Collected Date"])


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
		tms_lastname_firstname = unicodedata.normalize('NFKD', req["GetTombstoneDataRestIdResult"]["AlphaSort"]).encode('ascii', 'ignore')
		tms_title = unicodedata.normalize('NFKD', req["GetTombstoneDataRestIdResult"]["Title"]).encode('ascii', 'ignore')
		tms_object_number = unicodedata.normalize('NFKD', req["GetTombstoneDataRestIdResult"]["ObjectNumber"]).encode('ascii', 'ignore')
		tms_objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
		tms_department = unicodedata.normalize('NFKD', req["GetTombstoneDataRestIdResult"]["Department"]).encode('ascii', 'ignore')
		tms_SortNumber = req["GetTombstoneDataRestIdResult"]["SortNumber"]

		extract_name = path_artist.split('/')
		cleaned_name = extract_name[2].replace('_',' ')
		year_collected = tms_SortNumber[:6]

		c.writerow([bytes,tms_title,tms_lastname_firstname,tms_object_number,tms_objectid,tms_department,year_collected])


fileHandle.close()