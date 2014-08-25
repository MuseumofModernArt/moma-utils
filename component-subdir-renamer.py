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

# change this to the artwork directory
targetdir = '/path/to/artwork/folder'

dirobject = walklevel(targetdir)
for x in dirobject:
	if len(x[1]) == 1:

		drmc_obj_id = re.sub('.*---.*---.*---', '', x[0])
		print "Components for "+drmc_obj_id
		req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+drmc_obj_id))
		artistname = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
		worktitle = req["GetTombstoneDataRestIdResult"]["Title"]
		objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
		objectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
		year = req["GetTombstoneDataRestIdResult"]["Dated"]
		components = req["GetTombstoneDataRestIdResult"]["Components"]

		components_dict = json.loads(components)

		currentname = x[1]
		component_dir = currentname[0]

		for y in components_dict:
			for key, value in y.iteritems():
				if y["ComponentNumber"] == component_dir:
					print y["ComponentID"]
					print y["ComponentNumber"]
					newdirname = currentname[0]+"---"+str(y["ComponentID"])+"---"+str(drmc_obj_id)
		print newdirname
		os.rename(join(x[0],currentname[0]),join(x[0],newdirname))