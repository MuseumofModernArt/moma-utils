#!/usr/bin/env python

import bagit, datetime, time, argparse, os, sys, subprocess, filecmp, hashlib

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d_%H:%M:%S')

parser = argparse.ArgumentParser(description="Python tool for ingest from shuttle hard drives at MoMA")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the materials on the shuttle drive you wish to transfer.')
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
	for i in range (100):
		while True:
			data = f.read(block_size)
			if not data:
				break
			md5.update(data)
		sys.stdout.write("\r%d%%" %i)
		sys.stdout.flush()
	return md5.hexdigest()

def execute(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# Poll process for new output until finished
	while True:
		nextline = process.stdout.readline()
		if nextline == '' and process.poll() != None:
			break
		sys.stdout.write(nextline)
		sys.stdout.flush()
	output = process.communicate()[0]
	exitCode = process.returncode
	if (exitCode == 0):
		return output
	else:
		print "rysnc failed"

dirname = timestamp+'__'+args.title
fullpath = os.path.expanduser(os.path.normpath(args.output) + os.sep)+dirname

if not os.path.exists(fullpath):
	os.makedirs(fullpath)
	print "Made "+fullpath+" directory."

print "copying file(s)"

execute(["rsync", "-avP", os.path.expanduser(os.path.normpath(args.input)), fullpath])

# subprocess.call(["rsync", "-avP", "--partial", args.input, fullpath])

print "File(s) copied... bagging local copy..."
bagit.make_bag(fullpath, {'Contact-Name': args.name})

print "Files bagged... making list of bag hashes."
## read md5 into dictionary
baghashes = []
orighashes = []
for line in open(fullpath+"/manifest-md5.txt"):
	column = line.split("  ")
	baghashes.append(column[0])

print "Calculating MD5 hashes of files on original source media."
## calculate md5 for files on original media
for path, subdirs, files in os.walk(args.input):
	for name in files:
		origpath = os.path.join(path, name)
		f = open(origpath)
		thishash = md5_for_file(f)
		orighashes.append(thishash)
		#
		# thishash = hashlib.md5()
		# f = open(origpath)
		# while not endOfFile:
		# 	data = f.read(8192)
		# 	thishash.update(data)

print "Comparing hashes"
if comp (baghashes, orighashes) == True:
	print "All is well. The bagged files match the files on the original storage media."
else:
	print "Something went wrong. Checksum mismatch."