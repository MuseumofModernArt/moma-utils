#!/usr/bin/env python

import argparse, csv, urllib2, json, base64, getpass
from hurry.filesize import size, si

parser = argparse.ArgumentParser(description="script that uses Binder's API to add AIP size to the granular ingest report")
parser.add_argument('-i', '--input', type=str, required=True, help='source data file.')
parser.add_argument('-o', '--output', type=str, required=False, help='where to put output')
parser.add_argument('-u', '--username', type=str, help='Binder username')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify a report file')
if not (args.username):
	parser.error('you did not supply a username')

password = getpass.getpass("Enter your password: ")

firstline = True

with open(args.input, 'rb') as csvfile:
	c = csv.writer(open(args.output, "wb"))
	c.writerow(["ingest date","size","UUID"])
	orig_report = csv.reader(csvfile, delimiter=',')
	for row in orig_report:
		if firstline:
			firstline = False
			continue
		uuid = row[1]

		print "checking "+ uuid
		print "row check "+ row[0]
		
		if row[0] != "":
			request = urllib2.Request("http://drmc.museum.moma.org/api/aips/"+uuid)
			base64string = base64.encodestring('%s:%s' % (args.username, password)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string) 
			try:
				result = urllib2.urlopen(request)

				start_date = row[4]
				end_date = row[5]
				start_date_trimmed = start_date[:-10]
				end_date_trimmed = end_date[:-10]
				data = json.load(result)
				size = data['size']

				print start_date_trimmed, end_date_trimmed, size, uuid

				c.writerow([start_date_trimmed,end_date_trimmed,size,uuid])
			except urllib2.HTTPError, e:
				print "Could not find AIP! Error code "
				print e.args

