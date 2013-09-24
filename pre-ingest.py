#!/usr/bin/env python

import bagit, datetime, time, argparse, os, sys, subprocess, filecmp, hashlib, threading, json, urllib2

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d_%H:%M:%S')

parser = argparse.ArgumentParser(description="Python tool for ingest from shuttle hard drives at MoMA")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the materials on the shuttle drive you wish to transfer.')
parser.add_argument('-id', '--accessionid', type=str, required=True, help='objectid of the work.')
parser.add_argument('-o', '--output', type=str, default='~/Desktop/', help='Location you wish to store the bagged transfer. Defaults to desktop if not specified')
parser.add_argument('-n', '--name', type=str, help='Name of the person operating the script. This ends up the Bag metadata')
parser.add_argument('-t', '--title', type=str, default='untitled_shuttledrive_transfer', help='Name of the transfer. This is optional.')
args = parser.parse_args()



def comp(list1, list2):
	for val in list1:
		if val in list2:
			return True
	return False

def md5_for_file(f, block_size=8192):
	md5 = hashlib.md5()
	while True:
		data = f.read(block_size)
		if not data:
			break
		md5.update(data)
	return md5.hexdigest()

def execute(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class RepeatingTimer(threading._Timer):
	def run(self):
			while True:
				self.finished.wait(self.interval)
				if self.finished.is_set():
					return
				else:
					self.function(*self.args, **self.kwargs)

def status():
	print (""),

def bag_that():
	bagit.make_bag(fullpath, {'Contact-Name': args.name})


def hash_that():
	## read md5 into list
	baghashes = []
	orighashes = []
	for line in open(fullpath+"/manifest-md5.txt"):
		column = line.split("  ")
		baghashes.append(column[0])
	
	for path, subdirs, files in os.walk(args.input):
		for name in files:
			origpath = os.path.join(path, name)
			f = open(origpath)
			thishash = md5_for_file(f)
			orighashes.append(thishash)
	if comp (baghashes, orighashes) == False:
		print "Something went wrong. There is a mismatch between the bag hashes and hashes of the files on the original storage media."
	else:
		print "hashes match!"

objectid = args.accessionid
req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/Object/"+objectid))
artistname = req["GetTombstoneDataRestResult"]["DisplayName"]
worktitle = req["GetTombstoneDataRestResult"]["Title"]
objectnum = req["GetTombstoneDataRestResult"]["ObjectNumber"]
objectid = req["GetTombstoneDataRestResult"]["ObjectID"]
verbatim = artistname+"---"+worktitle+"---"+objectnum+"---"+objectid
sanitized = verbatim.replace (" ", "_")

# dirname = timestamp+'__'+args.title
dirname = sanitized
fullpath = os.path.expanduser(os.path.normpath(args.output) + os.sep)+dirname


if not os.path.exists(fullpath):
	os.makedirs(fullpath)
	print "Made "+fullpath+" directory."

print "\n==========================\ncopying file(s) with rsync \n=========================="
timer = RepeatingTimer(1.0, status)
timer.daemon = True
timer.start()
proc = subprocess.Popen(["rsync", "-avP", os.path.expanduser(os.path.normpath(args.input)), fullpath])
proc.wait()
timer.cancel()



print 'Bagging files....  ',
bag_that()
print '\b\b files bagged!'

print 'Verifying hashes....  ',
hash_that()


