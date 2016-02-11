#!/usr/bin/env python

import argparse, os, re, bagit

parser = argparse.ArgumentParser(description="script for doing automated QA on the Warhol scans")
parser.add_argument('-s', '--source', type=str, required=True, help='the root that contains the bags')
parser.add_argument('-d', '--destination', type=str, required=True, help='where to rsync bags that pass QA')
args = parser.parse_args()


re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
re2='---'	# Non-greedy match on filler
re3='((?:[a-z][a-z0-9_]*))'	# Variable Name 2
re4='---'	# Non-greedy match on filler
re5='((?:[a-z][a-z]+))'	# Word 1

pattern = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)

number_of_reels = 0
good_bags = 0
bad_bags = 0
matches = 0
mismatches = 0
bag_dict = {}

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
	print "there are "+str(number_of_reels)+" bags"
	print "checking name convention conformence"

	for dir in dirs:
		fullpath = args.source+'/'+dir
		bag_dict[fullpath] = {}
		if pattern.match(dir):
			matches += 1
			bag_dict[fullpath]['validname'] = 'true' 
		else:
			mismatches += 1
			bag_dict[fullpath]['validname'] = 'false'
		# check for mezz file bags, and when found make sure they have access files, and conform to structure
		if dir.endswith('mezz'):
			# make sure it contains a MOV file
			# make sure it contians a sub-dir with same name
			# make sure sub-dir contains manualNormalization dir, with a MOV file of same name inside
	print str(matches)+" bags meet the naming convention"
	print str(mismatches)+" bags failed the naming convention"
	
	# checking validity of bags
	for dir in dirs:
		fullpath = args.source+'/'+dir
		bag = bagit.Bag(fullpath)
		# print bag
		if bag.is_valid():
			# print "bag is valid"
			bag_dict[fullpath]['validbag'] = 'true'
			good_bags += 1
		else:
			bag_dict[fullpath]['validbag'] = 'false'
			bad_bags += 1
			# print ":("

print str(good_bags)+" Valid bags"
print str(bad_bags)+" Invalid bags"
print bag_dict

for key, value in bag_dict.iteritems():
	if value['validname'] == 'true' and value['validbag'] == 'true':
		print key+' <----- this is a good transfer ready to rsync'
		print 'trying rsync...'
		os.system("rsync -avrz "+key+" "+args.destination)
	else:
		print key+' <------ problem'


# for each folder in target DONE

	# if it is a mezz file (ends with ---mezz)
		# is there a manual normalization folder?
		# does it contain an access folder?
		# does it contain a file with the same name as the file in the /data root?
		# if it passes all these tests continue
		# else report the error and go on to the next folder

	# after rsync has finished, mv the folder to /ready for ingest











