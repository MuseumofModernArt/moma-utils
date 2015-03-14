#!/usr/bin/env python

import argparse, re, time,ast

parser = argparse.ArgumentParser(description="Python tool for generating performance statistics from Archivematica's Automation-tools log file")
parser.add_argument('-i', '--input', type=file, help='log file to read')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify a log file')

log = args.input

# x = 0
# l = 0

# regex1 = re.compile("New transfer candidates: set\(\['(.+)'\]\)")
# regex2 = re.compile(r'(\S+)\s+(\S{10} \S{8})\s*(\S.*)$')


# for line in log:
# 	start_transfer = regex1.search(line)
# 	timestamp = regex2.search(line)
# 	if start_transfer:
# 		l = l+1
# 		n = start_transfer.group(1)
# 		ntrim = n.split("/")[1]
# 		if timestamp:
# 			print timestamp.group(2)+" "+ntrim+"   line:  "+str(x)
# 	x = x+1
# print "total lines: "+str(x)
# print "lines where transfers are started: "+str(l)

x = 0

for line in log:
	match = re.match(r'(\S+)\s+(\S{10} \S{8})\s*(\S.*)$', line)
	if match:
		level = match.group(1)
		timestr = match.group(2)
		timestamp = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
		message = match.group(3)
		
		# # transfer candidates
		# match = re.match(r'.*New transfer candidates: set\((.*/.*)\)', message)
		# if match:
		# 	candidates = match.group(0)
		# 	candidates = candidates.split("/")[1][:-3]
		# 	if len(candidates) < 40:
		# 		print 'New transfer candidate at '+str(timestamp)+': ', candidates
		# 		x = x+1
		# 	continue

		# status info
		match = re.match(r'.*Status info: (.*)$', message)
		if match:
			info = ast.literal_eval(match.group(1))
			print 'Status info:', info
			continue

	# 	print 'Unrecognized message.'
	# else:
	# 	print 'Unrecognized line.'
print x
