#!/usr/bin/env python

import argparse, re, time,ast,json,urllib2

from datetime import datetime

parser = argparse.ArgumentParser(description="Python tool for generating performance statistics from Archivematica's Automation-tools log file")
parser.add_argument('-i', '--input', type=file, help='log file to read')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify a log file')

log = args.input

start_time = 0
stop_time = 0
trans_dict = dict()

def start():
	candidates = start_match.group(0)
	startidno = candidates.split("/")[1][:-3]
	start_time =  timestamp
	# print startidno+' started at '+start_time
	return (start_time, startidno)

def stop():
	info = stop_match.group(2)
	stopidno = info[10:]
	stop_time = timestamp
	uuid = stop_match.group(4)
	# print stopidno+' finished at '+stop_time+'\n'
	return (stop_time, stopidno, uuid)

for line in log:
	match = re.match(r'(\S+)\s+(\S{10} \S{8})\s*(\S.*)$', line)
	if match:
		level = match.group(1)
		timestr = match.group(2)
		# timestamp = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
		timestamp = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
		message = match.group(3)
		
		# find when new candidates are set
		start_match = re.match(r'.*New transfer candidates: set\((.*/.*)\)', message)
		if start_match:
			start_time = start()[0]
			start_idno = start()[1]
			# add idno to dictionary as key, add starttime as value 1
			trans_dict[start_idno] = [start_time,]
			continue

		# find when something is marked as complete
		stop_match = re.match(r"(.*u'status': u'COMPLETE'.*)\s*('name': u'.*---.*---.*)\s*(.*', u'path'.*)\s*(.*'.*-.*-.*-.*-.*)", message)
		if stop_match:
			stop_time = stop()[0]
			stop_idno = stop()[1]
			uuid = stop()[2][:-2][1:]
			# where idno matches in dict, add stoptime and UUID as values 2 and 3
			if trans_dict.has_key(stop_idno):
				trans_dict[stop_idno].append(stop_time)
				trans_dict[stop_idno].append(uuid)
			continue

for key in trans_dict:
	if len(trans_dict[key]) > 1:
		uuid = str(trans_dict[key][2])
		req = json.load(urllib2.urlopen("http://drmc.museum.moma.org/api/aips/"+uuid))
		print req
		AIPsize = req["size"]
		print "AIP UUID: "+uuid
		print "AIP Name: "+key
		print "Is this size: "+AIPsize
		duration = trans_dict[key][1]-trans_dict[key][0]
		print "Took this long: "+str(duration)+"\n"

