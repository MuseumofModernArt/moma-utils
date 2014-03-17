#!/usr/bin/env python

import bagit, datetime, time, argparse, os, sys, subprocess, filecmp, hashlib, threading, json, urllib2

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d_%H:%M:%S')

parser = argparse.ArgumentParser(description="Python tool for ingest from shuttle hard drives at MoMA")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the materials on the shuttle drive you wish to transfer.')
parser.add_argument('-id', '--objectid', type=str, required=True, help='objectid of the work.')
parser.add_argument('-o', '--output', type=str, default='~/Desktop/', help='Location you wish to store the bagged transfer. Defaults to desktop if not specified')
parser.add_argument('-n', '--name', type=str, help='Name of the person operating the script. This ends up the Bag metadata')
parser.add_argument('-t', '--title', type=str, default='untitled_shuttledrive_transfer', help='Name of the transfer. This is optional.')
args = parser.parse_args()


objectid = args.objectid
req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+objectid))
artistname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
worktitle = req["GetTombstoneDataRestIdResult"]["Title"]
objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
verbatim = "{}---{}---{}---{}".format(artistname, worktitle, objectnum, objectid)
print verbatim
#verbatim = artistname+"---"+worktitle+"---"+objectnum+"---"+objectid # .format(artistname, worktitle, objectnum, objectid)
sanitized = verbatim.replace (" ", "_")

# dirname = timestamp+'__'+args.title
dirname = sanitized
fullpath = os.path.expanduser(os.path.normpath(args.output) + os.sep)+dirname


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
	bagit.make_bag(fullpath, {'Contact-Name': args.name}, checksum = ['sha1'])

def hash_that():
	baghashes = []
	orighashes = []

	# create list of checksums in bag
	for line in open(fullpath+"/manifest-sha1.txt"):
		column = line.split("  ")
		baghashes.append(column[0])

	# if input is a directory
	if os.path.isdir(args.input):
		for path, subdirs, files in os.walk(args.input):
			for name in files:
				origpath = os.path.join(path, name)
				f = open(origpath)
				thishash = sha1_for_file(f)
				orighashes.append(thishash)

	# if input is an individual file
	else:
		f = open(args.input)
		thishash = sha1_for_file(f)
		orighashes.append(thishash)

	#compare list of hashes in bag with list of hashes calculated from original source
	if comp (baghashes, orighashes) == False:
		print "Something went wrong. There is a mismatch between the bag hashes and hashes of the files on the original storage media."
		print "Baghashes: "
		print baghashes
		print "Hashlib hashes of orig files: "
		print orighashes
	else:
		print "hashes match!"


if not os.path.exists(fullpath):
	os.makedirs(fullpath)
	print "Made "+fullpath+" directory."

print "\n==========================\ncopying file(s) with rsync \n=========================="
proc = subprocess.Popen(["rsync", "-avP", os.path.expanduser(os.path.normpath(args.input)), fullpath])
proc.wait()




print 'Bagging files....  ',
bag_that()
print '\b\b files bagged!'

print 'Verifying hashes....  ',
hash_that()


