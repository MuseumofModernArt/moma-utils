#!/usr/bin/env python

# CLI interface for providing directory name according to MoMA DRMC naming convention

import argparse, sys, json, urllib2, xerox

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

verbatim = "{}---{}---{}---{}".format(artistname.encode("utf-8"), worktitle.encode("utf-8"), objectnum, objectid)
#verbatim = artistname+"---"+worktitle+"---"+objectnum+"---"+objectid # .format(artistname, worktitle, objectnum, objectid)
sanitized = verbatim.replace (" ", "_")
sanitized = sanitized.translate(None, '()"/:,')
sanitized = sanitized.replace ("__", "_")

border = len(sanitized.decode("utf-8"))
border = border + 21

print "-" * border
print "Copied to clipboard: "+ sanitized.decode("utf-8")
print "-" * border

xerox.copy(sanitized.decode("utf-8"))