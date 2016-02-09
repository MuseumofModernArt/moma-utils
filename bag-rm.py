#!/usr/bin/env python

import bagit, argparse, os, sys, os.path

'''
This script is dedicated to those who hate .DS_store, Thumbs.db, and other kinds of annoying hidden files.

USAGE: python bag-rm.py -i [ path to dir you want to turn into a bag ]

edit the rm_these list below to set what files you want excluded from your bag. They will be deleted.

DISCLAIMER: this script is in no way intended to be used for production use. I'm not responsible if you muck up your stuff.

'''

rm_these = ['.DS_Store', 'Thumbs.db']

parser = argparse.ArgumentParser(description="Python tool for making BagIt bags, but excluding specific files")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to what you want to bag')
args = parser.parse_args()

for root, dirs, files in os.walk(args.input):
	for name in files:
		path = os.path.join(root, name)
		for i in rm_these:
			if name == i:
				print 'removing: '+path
				os.remove(path)

bag = bagit.make_bag(args.input)
