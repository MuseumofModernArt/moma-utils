#!/usr/bin/env python

import argparse, os, shutil

parser = argparse.ArgumentParser(description="script for making a bunch of random directories")
parser.add_argument('-t', '--target', type=str, required=True, help='where to put the test data')
parser.add_argument('-r', '--reels', type=int, required=True, help='how many "reels" to make')
parser.add_argument('-f', '--files', type=int, required=True, help='how many files per reel')
args = parser.parse_args()

target = args.target

x = 1
dpx_num = 0001

title = "this_is_a_title_"
reel = "reel_1_of_6"
sep = "---"

while (x <= args.reels):
	dirname = title+str(x)+sep+reel+sep+"scan"
	if os.path.isdir(target+'/'+dirname):
		shutil.rmtree(target+'/'+dirname)
		# print "deleting "+target+'/'+dirname
	os.mkdir(target+'/'+dirname)
	# print "just made "+target+'/'+dirname
	while (dpx_num <= args.files):
		filename = target+'/'+dirname+'/'+dirname+str(dpx_num)+".dpx"
		open(filename,'w')
		# print "writing"+filename
		dpx_num += 1
	dpx_num = 0001
	x += 1