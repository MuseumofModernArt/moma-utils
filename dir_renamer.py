#!/usr/bin/env python

# provides directory named according to MoMA DRMC standards

import argparse, sys, json, urllib2, os


parser = argparse.ArgumentParser(description="Python tool for getting the properly formated directory name for the DRMC")
parser.add_argument('-i', '--input', type=str, help='full path of the dir you want to rename')
parser.add_argument('-id', '--objectid', type=str, help='objectid of the work.')
parser.add_argument('-an', '--accessionnum', type=str, help='accession number of the work')
args = parser.parse_args()

if not (args.input):
    parser.error('you did not specify a path')


idnum = os.path.basename(os.path.normpath(args.input))

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
sanitized = sanitized.decode("utf-8")
normalized = os.path.normpath(args.input)
print "/Volumes/drmc/Collections_materials/Fluxus\ Collection/"+sanitized

print "-----------------------------------------------------------"
print "Here is your directory name: "+ sanitized
print "-----------------------------------------------------------"
print "Does this look right? (y/n)"
char = raw_input().lower()
if char == "y":
	os.rename(normalized, "/Volumes/drmc/Collections_materials/Fluxus\ Collection/"+sanitized)
	print
	print "-----------------------------------------------------------"
	print 
	print "-----------------------------------------------------------"
else:
	print "OK. Try again, human."