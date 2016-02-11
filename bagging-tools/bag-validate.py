#!/usr/bin/env python

import argparse, bagit
from pyfiglet import Figlet

parser = argparse.ArgumentParser(description="Helper for validating bags")
parser.add_argument('-i', '--input', type=str, help='absolute path of the uncompressed bag to validate')
args = parser.parse_args()

f = Figlet(font='slant')

if not args.input:
    parser.error('you did not specify a directory')

bag = bagit.Bag(args.input)

border = len(args.input)
border = border + 14

if bag.is_valid():
    print "=" * border
    print "BAG IS VALID: "+args.input
    print "=" * border
else:
    print f.renderText("INVALID BAG")
    print args.input