#!/usr/bin/env python
from __future__ import print_function
from requests.exceptions import HTTPError
import sqlite3 as lite
import sys, argparse, requests, getpass, csv


# The purpose of this script is to provide a report of what transfers
# have been sucsesfully processed by Archivematica's automation-tools,
# so that the original source of the transfer may be deleted since the
# materials are safely packaged and stored in an AIP.
#
# This mission is accomplished by looking at the sqlite database
# maintained by Archivematica's automation-tools, and talk to
# the Binder API in order to ensure that if automation-tools says
# it has processed an AIP, that this AIP has actually been 100%
# sucsesfully processed and is tracked in Binder.
# 
# This is necesary because if an automated transfer fails at any
# point in the workflow (for instance, normalization, or AIP storage),
# automation-tools is ignorant of this fact.

parser = argparse.ArgumentParser(description="Python tool for auditing Automation-Tool's database and making sure AIP is stored and tracked in Binder")
parser.add_argument('-i', '--input', type=str, help='sqlite database to read')
parser.add_argument('-u', '--username', type=str, help='Binder username')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify a database')
if not (args.username):
	parser.error('you did not supply a username')

password = getpass.getpass("Enter your password: ")

db = args.input
conn = lite.connect(db)
c = conn.cursor()
deletion_count = 0
reingest_count = 0
csvfile = open('delete_me.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['AIP uuid', 'original transfer path'])

# row headers are
# id, uuid, path, unit_type, status, microservice, current
for row in c.execute('SELECT * FROM unit where unit_type = "ingest"'):
	uuid = row[1]
	path = row[2]
	username = args.username
	auth = (username, password)
	url = "http://drmc.museum.moma.org/api/aips/"+uuid
	try:
		r = requests.get(url, auth=auth)
		r.raise_for_status()
		deletion_count += 1
		print (path+" can be deleted \n")
		# write row in CSV with AIP UUID and path
		writer.writerow([uuid, path])
	except HTTPError:
		print ('Could not find in Binder', r.url,'\n')
		reingest_count = reingest_count+1
		# write row in anothercsv with UUID
		# delete this row from sqliteDB
print (str(deletion_count)+" transfer sources that can be deleted")
print (str(reingest_count)+" transfers that need to be re-ingested")


# delete from unit where uuid = "4d8f31ad-1c77-4772-be14-40618d25e481";
# select * from unit where uuid = "4d8f31ad-1c77-4772-be14-40618d25e481";
