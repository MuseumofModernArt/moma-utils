#!/usr/bin/env python

import argparse, os, csv, subprocess

# this is a script for locating the DAM / DRMC integration metadata

parser = argparse.ArgumentParser(description="this is a script for locating the DAM / DRMC integration metadata")
parser.add_argument('-i', '--input', type=str, required=True, help='CSV of files missing metadata')
parser.add_argument('-s', '--search', type=str, required=True, help='path to backed up CSVs')
parser.add_argument('-o', '--output', type=str, required=False, help='where to put output new CSV to')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify an input file')
if not (args.search):
	parser.error('you did not specify a directory to search')

firstline = True

with open(args.input, 'rb') as csvfile:
	c = csv.writer(open(args.output, "wb"))
	c.writerow(["filename","ObjectID","Component Number", "dip_uuid"])
	i = csv.reader(csvfile, delimiter=',')
	for row in i:
		if firstline:
			firstline = False
			continue

		print "checking "+ row[0]

		p = subprocess.Popen(['grep', row[0], '*.csv'])




		
		# if row[0] != "":
		# 	request = urllib2.Request("http://drmc.museum.moma.org/api/aips/"+uuid)
		# 	base64string = base64.encodestring('%s:%s' % (args.username, password)).replace('\n', '')
		# 	request.add_header("Authorization", "Basic %s" % base64string) 
		# 	try:
		# 		result = urllib2.urlopen(request)

		# 		start_date = row[4]
		# 		end_date = row[5]
		# 		start_date_trimmed = start_date[:-10]
		# 		end_date_trimmed = end_date[:-10]
		# 		data = json.load(result)
		# 		size = data['size']

		# 		print start_date_trimmed, end_date_trimmed, size, uuid

		# 		c.writerow([start_date_trimmed,end_date_trimmed,size,uuid])
		# 	except urllib2.HTTPError, e:
		# 		print "Could not find AIP! Error code "
		# 		print e.args

