#!/usr/bin/env python

import os
import datetime
import re
import sqlite3
from hurry.filesize import size
from sys import stdout

i = datetime.datetime.now()
now = i.isoformat()

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                print str(total_size)+" bytes / "+str(size(total_size))+" counted"+" <------------ current position: "+start_path+" : "+f+"\n"location+": "+locations_dict[location][1]+"                                                       \r"
                for location in locations_dict:
            except OSError, e:
                print e
    return total_size

def updateSize():
    i = datetime.datetime.now().date()
    updatedate = i.isoformat()
    print "{} is the date".format(updatedate)
    conn = sqlite3.connect('/var/www/automation-audit/metrics.db')
    c = conn.cursor()

    query = c.execute("SELECT * FROM size WHERE Date=(?)",(updatedate,))
    one = c.fetchone()
    print "result is: {}".format(one)
    if one == None:
        print "Logging sizes for today..."
        c.execute("INSERT INTO size VALUES (?,'','','','','','','')",(updatedate,))
        for location in locations_dict:
            c.execute("UPDATE size SET "+location+"=(?) WHERE Date=(?)",(locations_dict[location][1],updatedate))
        conn.commit()
        conn.close()
    else:
        print "Already an entry for today - let's update those numbers"
        for location in locations_dict:
            c.execute("UPDATE size SET "+location+"=(?) WHERE Date=(?)",(locations_dict[location][1],updatedate))
        conn.commit()
        conn.close()

# the base bath of the DRMC as it is mounted on VMDRMC02
base_path_1 = '/home/archivesuser/moma/drmc/'
base_path_2 = '/mnt/pre-ingest/'

# a dictionary of the workflow dirs and their sizes
locations_dict = {'readyForIngest':[base_path_1+'ready_for_ingest-unbagged',''], 'readyForIngest2':[base_path_1+'ready_for_ingest-bagged',''], 'artworkBacklog':[base_path_1+'Artwork_level_backlog',''],'mpaBacklog':[base_path_1+'Artwork_level_backlog/_MPA',''], 'preIngestIsilon':[base_path_2+'staging',''], 'preIngest':[base_path_1+'pre-ingest_staging','']}

# for each location in the above dictionary
for location in locations_dict:
	#assemble the full path
	fullpath = locations_dict[location][0]
	#set this in the dictionary
	locations_dict[location][0] = fullpath
	# get the size
	filesize = get_size(fullpath)
	locations_dict[location][1] = filesize

updateSize()


