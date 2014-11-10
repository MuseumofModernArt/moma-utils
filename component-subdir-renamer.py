# run this on artwork directories with component sub-dirs, named with their component numbers

import os, json, urllib2, re
from os.path import join

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

# pre-ingest staging dir -- make sure this is right
targetdir = '/Volumes/drmc/Collections_materials/pre-ingest_staging/_run_component_script'

dirobject = walklevel(targetdir)
skip_target = iter(dirobject)
next(skip_target)

for x in skip_target:
	drmc_obj_id = re.sub('.*---.*---.*---', '', x[0])
	print x[0]
	req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+drmc_obj_id))
	artistname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
	worktitle = req["GetTombstoneDataRestIdResult"]["Title"]
	objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
	objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
	year = req["GetTombstoneDataRestIdResult"]["Dated"]
	components = req["GetTombstoneDataRestIdResult"]["Components"]

	components_dict = json.loads(components)

	dirlist = x[1]
	component_dir = dirlist[0]
	z = 0
	for y in components_dict:
		# print "looking for "+str(y)
		for q in dirlist:
			# print "checking "+ q
			# print "z = "+str(z)
			if y["ComponentNumber"] == q:
				print "Matched component ID "+str(y["ComponentID"])+" for component "+ str(y["ComponentNumber"])
				newdirname = q+"---"+str(y["ComponentID"])+"---"+str(drmc_obj_id)
				print "oldname = "+ join(x[0],q)
				print "newname = "+ join(x[0],newdirname)
				print
				os.rename(join(x[0],q),join(x[0],newdirname))
			# else:
			# 	print "no dirs for that component"
			# 	print
		z = z + 1
	print