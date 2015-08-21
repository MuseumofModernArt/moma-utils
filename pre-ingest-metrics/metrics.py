#!/usr/bin/env python

import os
import datetime
import re
import sqlite3

# this function returns a count of the immediate subdirectories as an integer
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                print fp
            except OSError, e:
                print e
    return total_size

# the base bath of the DRMC as it is mounted on VMDRMC02
base_path_1 = '/home/archivesuser/moma/drmc/'
base_path_2 = '/mnt/pre-ingest/'

# a dictionary of the workflow containing a nested data structure: the values are 1)directory name 2)placeholder for count of directories 3)placeholder list array of artwork folder names 4) placeholder for directory size in bytes
locations_dict = {'preIngest':[base_path_1+'pre-ingest_staging','',[''],''], 'readyForIngest':[base_path_1+'ready_for_ingest','',[''],''], 'readyForIngest2':[base_path_1+'ready_for_ingest_2','',[''],''], 'artworkBacklog':[base_path_1+'Artwork_level_backlog','',[''],''],'mpaBacklog':[base_path_1+'Artwork_level_backlog/_MPA','',[''],''], 'preIngestIsilon':[base_path_2+'staging','',[''],'']}

# for each location in the above dictionary
for location in locations_dict:
	#assemble the full path
	fullpath = locations_dict[location][0]
	#set this in the dictionary
	locations_dict[location][0] = fullpath
	#get the immediate subdirectories
	fullpath_listing = get_immediate_subdirectories(fullpath)
	#put them in the dictionary
	locations_dict[location][2] = fullpath_listing
	# count the length
	fullpath_size = len(fullpath_listing)
	locations_dict[location][1] = fullpath_size
	# get the size
	print get_size(fullpath)
	size = get_size(fullpath)
	locations_dict[location][3] = size
	print size
	# print locations_dict[location][1]

# The sqlite DB called "metrics" has 6 tables
# table 1: preIngest
# table 2: runComponent
# table 3: readyForIngest
# table 4: artworkBacklog
# table 5: counting
# table 6: size
#
# The structure of tables 1-4 is:
# +--------+----------------------------------------------+-------------+----------------+
# | ObjID  |                 folderName                   | appearedOn  | disappearedOn  |
# +--------+----------------------------------------------+-------------+----------------+
# | 169688 | Cohen_Jem---Little_Flags---F2013.43---169688 | 2015-01-05  | 2015-03-24     |
# +--------+----------------------------------------------+-------------+----------------+
#
# The structure of table 5 is:
# +------------+-----------------------+------------+---------------+------------------+--+
# |    Date    |  artworkLevelBacklog  | preIngest  |  runComponent |  readyForIngest  |  |
# +------------+-----------------------+------------+---------------+------------------+--+
# | 2015-01-01 |                   350 |         70 |             0 |              500 |  |
# | 2015-01-02 |                   350 |         70 |             0 |              500 |  |
# | 2015-01-03 |                   348 |         73 |             0 |              502 |  |
# | 2015-01-04 |                   330 |         80 |             2 |              538 |  |
# +------------+-----------------------+------------+---------------+------------------+--+
#
# The output of the artwork level stats could look something like this
# +-----------+-----------------------------+------------+---------------+------------------+
# |  Obj num  |            Title            | pre-ingest | run-component | ready-for-ingest |
# +-----------+-----------------------------+------------+---------------+------------------+
# | 68.2015.1 | Wing House Helsinki Finland | 90 days    | 10 days       | 2 days           |
# | F2013.43  | Little Flags                | 30 days    | 5 days        | 10 days          |
# +-----------+-----------------------------+------------+---------------+------------------+
#

i = datetime.datetime.now()
now = i.isoformat()

#######
####### this first function is to add any newly appeared directories to the database, and log the present date as the "appeared on" date
####### 
def dbSync(location):
	a = 0
	b = 0
	artworklist = locations_dict[location][2]
	for artwork in artworklist:
		objectID = re.sub('.*---.*---.*---', '', artwork)
		if objectID != "" and len(objectID) < 10 and isinstance(objectID, int) == True:
		# these conditions mitigate parsing errors for cases when the object ID is missing from the folder name
			conn = sqlite3.connect('/var/www/automation-audit/metrics.db')
			c = conn.cursor()
			query = c.execute("SELECT * FROM {0} WHERE ObjID = '{1}' ;".format(location,objectID))
			one = c.fetchone()
			if one != None:
				# print "{0} is already in the {1} DB".format(one,location)
				a = a+1
			else:
				# print "{0} will be added to the {1} table".format(objectID,location)
				b = b+1
				c.execute("INSERT INTO "+location+" VALUES (?,?,?,'')",(objectID,buffer(artwork),now))
				conn.commit()
				conn.close()
	print "{0} folders that are already tracked in the {1} DB".format(a, location)
	print "{0} folders that have been added to the {1} DB".format(b, location)


#######
####### this second function is to look through the database, and see if anything in the database is no longer in the directory -- if so, log the date
#######
def checkForMoves(location):
	a = 0
	b = 0
	artworklist = locations_dict[location][2]
	conn = sqlite3.connect('/var/www/automation-audit/metrics.db')
	c = conn.cursor()
	query = c.execute("SELECT * FROM {0}".format(location))
	for row in query:
		objectID = row[0]
		templist = []
		for artwork in artworklist:
			artworkObjectID = re.sub('.*---.*---.*---', '', artwork)
			if artworkObjectID != "" and len(artworkObjectID) < 10 and isinstance(artworkObjectID, int) == True:
				templist.append(int(artworkObjectID))
		if objectID in templist:
			# print "{0} is in the {1} table and still in the {2} dir".format(objectID,location,locations_dict[location][0])
			a = a+1
		else:
			# print "something has disappeared from the {0} dir".format(locations_dict[location][0])
			c.execute("UPDATE "+location+" SET disappearedOn=(?) WHERE ObjID=(?)",(now,objectID))
			b = b+1
	print "{} folders have not moved".format(a)
	print "{} folders have disappeared".format(b)
	conn.commit()
	conn.close()

def updateCounts():
	i = datetime.datetime.now().date()
	updatedate = i.isoformat()
	print "{} is the date".format(updatedate)
	conn = sqlite3.connect('/var/www/automation-audit/metrics.db')
	c = conn.cursor()

	query = c.execute("SELECT * FROM counting WHERE Date=(?)",(updatedate,))
	one = c.fetchone()
	print "result is: {}".format(one)
	if one == None:
		print "Logging counts for today..."
		c.execute("INSERT INTO counting VALUES (?,'','','','','','','')",(updatedate,))
		for location in locations_dict:
			c.execute("UPDATE counting SET "+location+"=(?) WHERE Date=(?)",(locations_dict[location][1],updatedate))
		conn.commit()
		conn.close()
	else:
		print "Already an entry for today - let's update those numbers"
		for location in locations_dict:
			c.execute("UPDATE counting SET "+location+"=(?) WHERE Date=(?)",(locations_dict[location][1],updatedate))
		conn.commit()
		conn.close()




for location in locations_dict:
	print 'moving on to %s table' % location
	dbSync(location)
	checkForMoves(location)
updateCounts()
