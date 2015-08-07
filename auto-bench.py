#!/usr/bin/env python
from __future__ import division
import argparse, re, time, ast, json, requests, base64, getpass
from hurry.filesize import size, si
from requests.exceptions import HTTPError
from datetime import datetime


parser = argparse.ArgumentParser(description="Python tool for generating performance statistics from Archivematica's Automation-tools log file")
parser.add_argument('-i', '--input', type=file, help='log file to read')
parser.add_argument('-u', '--username', type=str, help='Binder username')
args = parser.parse_args()

if not (args.input):
	parser.error('you did not specify a log file')
if not (args.username):
	parser.error('you did not supply a username')

password = getpass.getpass("Enter your password: ")

log = args.input
start_count = 0
stop_count = 0
startstop_match = 0
start_time = 0
stop_time = 0
trans_dict = dict()
final_total=0
total_bytes=0

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

def getMin(s):
	l = str(s).split(':')
	secs = float(l[0]) * 3600 + float(l[1]) * 60 + float(l[2])
	mins = secs/60
	return mins

for line in log:
	match = re.match(r'(\S+)\s+(\S{10} \S{8})\s*(\S.*)$', line)
	if match:
		level = match.group(1)
		timestr = match.group(2)
		# timestamp = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
		timestamp = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
		message = match.group(3)
		
		# find when new candidates are set
		start_match = re.match(r".*New transfer candidates: set\((\['.*/.*\])\)", message)
		if start_match:
			start_time = start()[0]
			start_idno = start()[1]
			# add idno to dictionary as key, add starttime as value 1
			trans_dict[start_idno] = [start_time,]
			start_count=start_count+1
			continue

		# find when something is marked as complete
		stop_match = re.match(r"(.*u'status': u'COMPLETE'.*)\s*('name': u'.*---.*---.*)\s*(.*', u'path'.*)\s*(.*'.*-.*-.*-.*-.*)", message)
		if stop_match:
			stop_time = stop()[0]
			stop_idno = stop()[1]
			uuid = stop()[2][:-2][1:]
			stop_count=stop_count+1
			# where idno matches in dict, add stoptime and UUID as values 2 and 3
			if trans_dict.has_key(stop_idno):
				trans_dict[stop_idno].append(stop_time)
				trans_dict[stop_idno].append(uuid)
				startstop_match = startstop_match+1
			continue

print "found this many starting lines "+str(start_count)
print "found this many stopping lines "+str(stop_count)
print "and this many corresponded "+str(startstop_match)


for key in trans_dict:
	if len(trans_dict[key]) > 1:
		uuid = str(trans_dict[key][2])
		print "AIP UUID "+uuid
		print "AIP name: "+key
		username = args.username
		auth = (username, password)
		url = "http://drmc.museum.moma.org/api/aips/"+uuid
		try:
			r = requests.get(url, auth=auth)
			r.raise_for_status()
		except HTTPError:
			print 'Could not find in Binder', r.url,'\n'
		else:
			final_total=final_total+1
			AIPsize = float(r.json()['size'])
			duration = trans_dict[key][1]-trans_dict[key][0]
			durMin = getMin(duration)
			avg = AIPsize/durMin
			perhour = avg*60
			total_bytes=total_bytes+perhour
			print "AIP size: ", size(AIPsize, system=si)
			print "AIP time spent in Archivematica "+str(duration)
			# print "This many minutes: "+str(getMin(duration))
			# print "Bytes per minute: "+str(avg)
			print size(avg, system=si)+" per minute"
			print size(perhour, system=si)+" per hour" 
			print "\n"
print "Was able to find full data for "+str(final_total)+" AIPs"
print "Average speed of processing: "+str(size(total_bytes/final_total))+" per hour"