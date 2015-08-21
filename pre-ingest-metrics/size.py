#!/usr/bin/env python

import os
import datetime
import re
import sqlite3

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                print total_size+" bytes counted"+" ::::: "+fp
            except OSError, e:
                print e
    return total_size

# the base bath of the DRMC as it is mounted on VMDRMC02
base_path_1 = '/home/archivesuser/moma/drmc/'
base_path_2 = '/mnt/pre-ingest/'

# a dictionary of the workflow dirs and their sizes
locations_dict = {'readyForIngest':[base_path_1+'ready_for_ingest',''], 'readyForIngest2':[base_path_1+'ready_for_ingest_2',''], 'artworkBacklog':[base_path_1+'Artwork_level_backlog',''],'mpaBacklog':[base_path_1+'Artwork_level_backlog/_MPA',''], 'preIngestIsilon':[base_path_2+'staging',''], 'preIngest':[base_path_1+'pre-ingest_staging','']}


# for each location in the above dictionary
for location in locations_dict:
	#assemble the full path
	fullpath = locations_dict[location][0]
	#set this in the dictionary
	locations_dict[location][0] = fullpath
	# get the size
	print get_size(fullpath)
	size = get_size(fullpath)
	locations_dict[location][3] = size
	print size
