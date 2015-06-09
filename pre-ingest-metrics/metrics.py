import os
import datetime
import re
import sqlite3

# this bit is for getting the basic counts of the directories
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

base_path = '/Volumes/drmc/Collections_materials/'
locations_dict = {'preIngest':['pre-ingest_staging','',['']], 'runComponent':['pre-ingest_staging/_run_component_script','',['']], 'readyForIngest':['ready_for_ingest','',['']], 'artworkBacklog':['Artwork_level_backlog','',['']]}

for location in locations_dict:
	fullpath = base_path+locations_dict[location][0]
	locations_dict[location][0] = fullpath
	fullpath_listing = get_immediate_subdirectories(fullpath)
	locations_dict[location][2] = fullpath_listing
	fullpath_size = len(fullpath_listing)
	locations_dict[location][1] = fullpath_size
	print locations_dict[location][1]

# The sqlite DB called "metrics" has 4 tables
# table 1: preIngest
# table 2: runComponent
# table 3: readyForIngest
# table 4: artworkBacklog
# table 5: counts
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
# Here is some pseudo code for filling in metrics.pre-ingest (same logic for run-component and ready-for-ingest)...
# List pre-ingest dir with one level of recursion --- put results in a dictionary called dirDict
#
# in theory those two loops should be all that is needed... I think.

i = datetime.datetime.now()
now = i.isoformat()

#######
####### this first loop is to add any newly appeared directories to the database, and log the present date as the "appeared on" date
####### 
def dbSync(location):
	artworklist = locations_dict[location][2]
	for artwork in artworklist: ######  <-----------------------------------this is currently hard-coded... need to think about how to make it iterate through a list of the locations
		objectID = re.sub('.*---.*---.*---', '', artwork)
		if objectID != "" and len(objectID) < 10:
		# these conditions mitigate parsing errors for cases when the object ID is missing from the folder name
			conn = sqlite3.connect('metrics.db')
			c = conn.cursor()
			query = c.execute("SELECT * FROM {0} WHERE ObjID = '{1}' ;".format(location,objectID))
			one = c.fetchone()
			if one != None:
				print "{0} is already in the {1} DB".format(one,location)
			else:
				print "{0} will be added to the {1} table".format(objectID,location)
				c.execute("INSERT INTO "+location+" VALUES (?,?,?,'')",(objectID,buffer(artwork),now))
				conn.commit()
				conn.close()

for location in locations_dict:
	print 'moving on to %s table' % location
	dbSync(location)

#######
####### this second loop is to look through the database, and see if anything in the database is no longer in the directory
#######
# for row in metrics.pre-ingest
# 	ObjID = first row
#	search dirDict for ObjID
#	if ObjID is not in dirDict
# 		update row[disappeared on] with current date
#




