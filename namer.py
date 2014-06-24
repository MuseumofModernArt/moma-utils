#!/usr/bin/env python

# provides directory named according to MoMA DRMC standards

import argparse, sys, json, urllib2


parser = argparse.ArgumentParser(description="Python tool for getting the properly formated directory name for the DRMC")
parser.add_argument('-id', '--objectid', type=str, help='objectid of the work.')
parser.add_argument('-an', '--accessionnum', type=str, help='accession number of the work')
args = parser.parse_args()

if not (args.objectid or args.accessionnum):
    parser.error('you did not specify a work')

if args.objectid != None:
	idnum = args.objectid
	req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+idnum))
	artistname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
	worktitle = req["GetTombstoneDataRestIdResult"]["Title"]
	objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
	objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
	year = req["GetTombstoneDataRestIdResult"]["Dated"]
elif args.accessionnum != None:
	idnum = args.accessionnum
	req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/Object/"+idnum))
	artistname = req["GetTombstoneDataRestResult"]["AlphaSort"]
	worktitle = req["GetTombstoneDataRestResult"]["Title"]
	objectnum = req["GetTombstoneDataRestResult"]["ObjectNumber"]
	objectid = req["GetTombstoneDataRestResult"]["ObjectID"]
	year = req["GetTombstoneDataRestResult"]["Dated"]

verbatim = "{}---{}---{}---{}".format(artistname, worktitle, objectnum, objectid)
print verbatim
#verbatim = artistname+"---"+worktitle+"---"+objectnum+"---"+objectid # .format(artistname, worktitle, objectnum, objectid)
sanitized = verbatim.replace (" ", "_")


print "-----------------------------------------------------------"
print worktitle+" ("+year+") by "+artistname
print "-----------------------------------------------------------"
print "Does this look right? (y/n)"
char = raw_input().lower()
if char == "y":
	print
	print "-----------------------------------------------------------"
	print "Here is your directory name: "+ sanitized
	print "-----------------------------------------------------------"
else:
	print "OK. Try again, human."