#!/usr/bin/env python

import bagit, datetime, time, argparse, os, subprocess, filecmp, hashlib

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d_%H:%M:%S')

parser = argparse.ArgumentParser(description="Python tool for ingest from shuttle hard drives at MoMA")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the materials on the shuttle drive you wish to transfer.')
parser.add_argument('-o', '--output', type=str, default='~/Desktop/', help='Location you wish to store the bagged transfer. Defaults to desktop if not specified')
parser.add_argument('-n', '--name', type=str, default='untitled_shuttledrive_transfer', help='Name of the transfer. This is optional.')
args = parser.parse_args()

dirname = timestamp+'__'+args.name
fullpath = os.path.expanduser(os.path.normpath(args.output) + os.sep)+dirname

if not os.path.exists(fullpath):
	os.makedirs(fullpath)
	print "Made "+fullpath+" directory."


subprocess.call(["rsync", "-a", "--partial", args.input, fullpath])

bagit.make_bag(fullpath, {'Contact-Name': 'Ben Fino-Radin'})


## read md5 into dictionary
baghashes = []
orighashes = []
for line in open(fullpath+"/manifest-md5.txt"):
    column = line.split("  ")
    baghashes.append(column[0])

## calculate md5 for files on original media
for path, subdirs, files in os.walk(args.input):
	for name in files:
		origpath = os.path.join(path, name)
		thishash = hashlib.md5()
		f = open(origpath)
		data = f.read()
		thishash.update(data)
		orighashes.append(thishash.hexdigest())


def comp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False

if comp (baghashes, orighashes) == True:
	print "All is well. The bagged files match the files on the original storage media."
else:
	print "Something went wrong. Checksum mismatch."