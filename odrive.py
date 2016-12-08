#!/usr/bin/env python

import glob
import os
import re


'''
# tool for MoMA O drive migration
# will create "artist level" folders and move object level folders inside

Pseudo code
1. crawl folders 2 levels deep
2. for folder:
	if folder matches *---*---*---* pattern:
		a. if artist level folder already exists
				aa. move object level folder inside
				bb. rename object level folder to folder[2]---folder[1] 
		b. else
			aa. create new folder using first part of name
			bb. move object level folder inside
			cc. rename object level folder to folder[2]---folder[1]
'''

# pattern for object level folders
re1='.*'	
re2='---'
pattern = re.compile(re1+re2+re1+re2+re1+re2+re1,re.IGNORECASE|re.DOTALL)


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


path = '/Volumes/Dept/CONSERV/All Conservation/0000 Media/1 Artists'

walker = walklevel(path)



for folder in walker:
	objectlevel_dirs = []
	artist_dirs = []
	print '\n\n'+"Listing "+ folder[0]
	for subdir in folder[1]:
		# print subdir
		if pattern.match(subdir):
			# print subdir
			objectlevel_dirs.append(subdir)
			# print subdir.split('---')
		else:
			artist_dirs.append(subdir)
		for directory in objectlevel_dirs:
			artistname = directory.split('---')
			print artistname[0]
			if artistname in artist_dirs:
				print "match!!!"
	print artist_dirs

	# print objectlevel_dirs





