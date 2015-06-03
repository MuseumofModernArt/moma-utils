import os
import datetime

# this bit is for getting the basic counts of the directories
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

backlog = get_immediate_subdirectories('/Volumes/drmc/Collections_materials/Artwork_level_backlog')
preIngestStaging = get_immediate_subdirectories('/Volumes/drmc/Collections_materials/pre-ingest_staging')
runComponent = get_immediate_subdirectories('/Volumes/drmc/Collections_materials/pre-ingest_staging/_run_component_script')
readyForIngest = get_immediate_subdirectories('/Volumes/drmc/Collections_materials/ready_for_ingest/')

print datetime.datetime.now()
print "Artwork Level Backlog: {}".format(len(backlog))
print "Pre-ingest staging area: {}".format(len(preIngestStaging))
print "Run Component dir: {}".format(len(runComponent))
print "Ready for ingest (automation): {}".format(len(readyForIngest))


# This bit is for getting a more specific, artwork-level way of tracking things.
# The intent is for the script to track a folder's movement through the stages
#
# I am going to make a sqlite DB called "metrics" with 4 tables
# table 1: counts
# table 2: pre-ingest
# table 3: run-component
# table 4: ready-for-ingest
#
# The structure of metrics.counts could look something like this:
# +------------+-----------------------+------------+---------------+------------------+--+
# |    Date    | Artwork-level Backlog | Pre-ingest | Run-component | Ready-for-ingest |  |
# +------------+-----------------------+------------+---------------+------------------+--+
# | 2015-01-01 |                   350 |         70 |             0 |              500 |  |
# | 2015-01-02 |                   350 |         70 |             0 |              500 |  |
# | 2015-01-03 |                   348 |         73 |             0 |              502 |  |
# | 2015-01-04 |                   330 |         80 |             2 |              538 |  |
# +------------+-----------------------+------------+---------------+------------------+--+
#
# The structure of metrics.pre-ingest, as well as run-component, and ready-for-ingest could look something like this
# +--------+----------------------------------------------+-------------+----------------+
# | ObjID  |                 Folder name                  | appeared on | disappeared on |
# +--------+----------------------------------------------+-------------+----------------+
# | 169688 | Cohen_Jem---Little_Flags---F2013.43---169688 | 2015-01-05  | 2015-03-24     |
# +--------+----------------------------------------------+-------------+----------------+
#
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
#######
####### this first loop is to add any newly appeared directories to the database, and log the present date as the "appeared on" date
####### 
# for item in dirDict
# 	dirObjID = item[prase out object id]
# 	query = select * from metrics.pre-ingest where ObjID is dirObjID
# 	if query is empty
# 		write a row to metrics.pre-ingest with dirObjID, item (path), and current date
#
#######
####### this second loop is to look through the database, and see if anything in the database is no longer in the directory
#######
# for row in metrics.pre-ingest
# 	ObjID = first row
#	search dirDict for ObjID
#	if ObjID is not in dirDict
# 		update row[disappeared on] with current date
#
#
# in theory those two loops should be all that is needed... I think.