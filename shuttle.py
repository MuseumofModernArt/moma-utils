#!/usr/bin/env python

import bagit, sys, datetime, time, argparse

'''
step 1: env variable A is the path to the materials on the source drive
		env variable B is the destination
		env variable C is the "name" of the transfer
step 2: make dir at env variable B --or-- if no env variable B, then on ~/Desktop that is date/timestamp + name of volume + "name"
step 3: move entire contents of env variable A to env variable B
step 4: bagit
step 5: 
'''

epoch = time.time()
timestamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d_%H:%M:%S')


parser = argparse.ArgumentParser(description="work in progres...")

parser.add_argument('-i', '--input', type=str, required=True,
					help='The full path to the materials on the shuttle drive you wish to transfer.')
parser.add_argument('-n', '--name', type=str, default='untitled_shuttledrive_transfer',
					help='Name of the transfer. This is optional.')

args = parser.parse_args()

dirname = timestamp+'__'+args.input+'__'+args.name

print dirname

# if not os.path.exists(dirname):
#     os.makedirs(dirname)


