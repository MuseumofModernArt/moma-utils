#!/usr/bin/env python

import subprocess, argparse

parser = argparse.ArgumentParser(description="Python tool for comparing the output of video characterization tools")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to the file you want to analyze.')
args = parser.parse_args()

cmnd = ['time','/Users/bfino/Downloads/bagit-4.4/bin/bag','baginplace', args.input]
# cmnd = ['time','echo','"test"']
p = subprocess.Popen(cmnd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out, err = p.communicate()
print p.communicate()

# print

# print out


# print err
# print out
# print p.communicate()