#!/usr/bin/env python

import bagit, datetime, time, argparse, os, sys, subprocess, filecmp, hashlib, threading, json, urllib2

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%H:%M:%S')

parser = argparse.ArgumentParser(description="Tool for acquiring / bagging materials at MoMA")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the materials on the shuttle drive you wish to transfer.')
parser.add_argument('-id', '--objectid', type=str, required=True, help='objectid of the work.')
parser.add_argument('-n', '--name', type=str, help='Name of the person operating the script. This ends up the Bag metadata')
parser.add_argument('-t', '--title', type=str, default='untitled_shuttledrive_transfer', help='Name of the transfer. This is optional.')
args = parser.parse_args()

objectid = args.objectid
req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+objectid))
artistname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
worktitle = req["GetTombstoneDataRestIdResult"]["Title"]
objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
year = req["GetTombstoneDataRestIdResult"]["Dated"]
verbatim = "{}---{}---{}---{}".format(artistname, worktitle, objectnum, objectid)
print verbatim
#verbatim = artistname+"---"+worktitle+"---"+objectnum+"---"+objectid # .format(artistname, worktitle, objectnum, objectid)
sanitized = verbatim.replace (" ", "_")

dirname = sanitized
fullpath = os.path.expanduser(os.path.normpath(dirname) + os.sep)+dirname

def comp(list1, list2):
	for val in list1:
		if val in list2:
			return True
	return False

def sha1_for_file(f, block_size=8192):
	sha1 = hashlib.sha1()
	while True:
		data = f.read(block_size)
		if not data:
			break
		sha1.update(data)
	return sha1.hexdigest()

def execute(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def status():
	print (""),

def bag_that():
	bagit.make_bag(fullpath, {'Contact-Name': args.name, 'Timestamp':timestamp}, checksum = ['sha1'])


print "-----------------------------------------------------------"
print worktitle+" ("+year+") by "+artistname
print "-----------------------------------------------------------"
print "Does this look right? (y/n)"
char = raw_input().lower()
if char == "y":
	if not os.path.exists(fullpath):
		os.makedirs(fullpath)
		print "Made "+fullpath+" directory."

	print 'Bagging files....  ',
	bag_that()
	print '\b\b files bagged!'

else:
	print "ok I won't do anything in that case"