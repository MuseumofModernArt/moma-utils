#!/usr/bin/env python

import argparse, os, shutil, bagit
from hurry.filesize import size

# In testing our workflows, we often need sample data.
# This script is used for generating N number of directories, containing X number of files, of Y size.
# It was written specifically for testing DPX ingest automation workflows. 

parser = argparse.ArgumentParser(description="script for making a bunch of directories with a bunch of files in them")
parser.add_argument('-t', '--target', type=str, required=True, help='where to put the test data')
parser.add_argument('-r', '--reels', type=int, required=True, help='how many "reels" to make')
parser.add_argument('-f', '--files', type=int, required=True, help='how many files per reel')
parser.add_argument('-fs', '--filesize', type=int, default='12000000', required=False, help='size of files in bytes. defaults to 12MB')
args = parser.parse_args()

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

target = args.target

x = 1
dpx_num = 1
filesize = 0

title = "this_is_a_title_"
reel = "reel_1_of_6"
sep = "---"

while (x <= args.reels):
	dirname = title+str(x)+sep+reel+sep+"scan"
	if os.path.isdir(target+'/'+dirname):
		shutil.rmtree(target+'/'+dirname)
		# delete the dir if it exists already
	os.mkdir(target+'/'+dirname)
	os.mkdir(target+'/'+dirname+'/'+dirname)
	# make the dir
	while (dpx_num <= args.files):
		filename = target+'/'+dirname+'/'+dirname+'/'+dirname+str(dpx_num)+".dpx"
		print "Dir "+str(x)+" of "+str(args.reels)+" ----- file "+str(dpx_num)+" of "+str(args.files)+" ----- total filesize: "+str(size(filesize))
		with open(filename,'wb') as fout:
			fout.write(os.urandom(args.filesize))
		filesize += args.filesize
		# write the file
		dpx_num += 1
	filesize += filesize
	print filesize
	dpx_num = 1
	x += 1

for subdir, dirs, files in walklevel(target, 0):
	for dir in dirs:
		bag = bagit.make_bag(target+'/'+dir)
