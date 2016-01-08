#!/usr/bin/env python

import argparse, os, re

parser = argparse.ArgumentParser(description="script for doing automated QA on the Warhol scans")
parser.add_argument('-s', '--source', type=str, required=True, help='the root that contains the bags')
# parser.add_argument('-d', '--destination', type=str, required=True, help='where to send bags that pass QA')
args = parser.parse_args()


re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
re2='---'	# Non-greedy match on filler
re3='((?:[a-z][a-z0-9_]*))'	# Variable Name 2
re4='---'	# Non-greedy match on filler
re5='((?:[a-z][a-z]+))'	# Word 1

pattern = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)


number_of_reels = 0

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

for subdir, dirs, files in walklevel(args.source, 0):
	for dir in dirs:
		number_of_reels += 1
	print "there are "+str(number_of_reels)+" reels to check"
	print "checking name convention conformence for reel folders"
	matches = 0
	mismatches = 0
	for dir in dirs:
		# print "check"
		if pattern.match(dir):
			matches += 1 
			# print "match!"
		else:
			mismatches += 1
			# print "fail"
	print str(matches)+" reels meet the naming convention"
	print str(mismatches)+" reels failed the naming convention"









# for each folder in target

	# does it adhere to the naming convention?

	# if it is a mezz file (ends with ---mezz)
		# is there a manual normalization folder?
		# does it contain an access folder?
		# does it contain a file with the same name as the file in the /data root?
		# if it passes all these tests continue
		# else report the error and go on to the next folder

	# are all the files present? do a bag verify complete

	# do a bag verify valid

	# if everything has passed, rsync the folder to /staging for bag pipelien

	# after rsync has finished, mv the folder to /ready for ingest