#!/usr/bin/env python

import argparse, csv, re

parser = argparse.ArgumentParser(description="script to look at the works listed in the MoMA dataset that are from the 60s")
parser.add_argument('-i', '--input', type=str, required=True, help='source data file.')
parser.add_argument('-o', '--output', type=str, required=False, help='where to put output')
args = parser.parse_args()



with open(args.input, 'rb') as csvfile:
	c = csv.writer(open(args.output, "wb"))
	c.writerow(["Title","Artist","ArtistBio","Date","Medium","Dimensions","CreditLine","MoMANumber","Classification","Department","DateAcquired","CuratorApproved","ObjectID","URL"])
	momadata = csv.reader(csvfile, delimiter=',')
	for row in momadata:
		sixties = re.compile("196.-..-..")
		if sixties.match(row[10]):
			print row[0]+" "+row[1]+" "+row[10]+" "+row[12]+" "+row[13]
			c.writerow(row)
	