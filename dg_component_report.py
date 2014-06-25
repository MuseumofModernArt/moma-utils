import fnmatch
import os
import os.path
import collections
import sys
import re
import argparse
import subprocess
import json
import urllib2
import csv
import codecs
import cStringIO

#setup
drmc_path = "/Volumes/drmc/Collections_materials"
regexp = re.compile('.*---.*---.*---.*')

parser = argparse.ArgumentParser(description="Report generator for acessing discrepancies between TMS cataloging and the contents of the DRMC")
parser.add_argument('-i', '--input', type=str, required=True, help='The full path to CSV report to read in from TMS.')
args = parser.parse_args()

#UTF-8 csv setup
class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


#directory walker
WalkedDir = collections.namedtuple("WalkedDir", "path subdirs files depth")

def filter_walk(top, file_pattern=None, dir_pattern=None, depth=None, onerror=None, followlinks=False, onloop=None):
    """filter_walk is similar to os.walk, but offers the following additional features:
        - yields a named tuple of (path, subdirs, files, depth)
        - allows a recursion depth limit to be specified
        - allows independent glob-style filters for filenames and subdirectories
        - emits a message to stderr and skips the directory if a symlink loop is encountered when following links

       Selective walks are always top down, as the directory listings must be altered to provide
       the above features.

       If not None, depth must be at least 0. A depth of zero can be useful to get separate
       filtered subdirectory and file listings for a given directory.

       onerror is passed to os.walk to handle os.listdir errors
       followlinks is passed to os.walk and enables the symbolic loop detection
       onloop (if provided) can be used to override the default symbolic loop handling. It is
       called with the directory path as an argument when a loop is detected. Any false return
       value will skip the directory as normal, any true value means the directory will be processed.
    """
    if depth is not None and depth < 0:
        msg = "Depth limit must be None or greater than 0 ({!r} provided)"
        raise ValueError(msg.format(depth))
    if onloop is None:
        def onloop(path):
            msg = "Symlink {!r} refers to a parent directory, skipping\n"
            sys.stderr.write(msg.format(path))
            sys.stderr.flush()
    if followlinks:
        real_top = os.path.abspath(os.path.realpath(top))
    sep = os.sep
    initial_depth = top.count(sep)
    for path, walk_subdirs, files in os.walk(top, topdown=True,
                                             onerror=onerror,
                                             followlinks=followlinks):
        # Check for symlink loops
        if followlinks and os.path.islink(path):
            # We just descended into a directory via a symbolic link
            # Check if we're referring to a directory that is
            # a parent of our nominal directory
            relative = os.path.relpath(path, top)
            nominal_path = os.path.join(real_top, relative)
            real_path = os.path.abspath(os.path.realpath(path))
            path_fragments = zip(nominal_path.split(sep), real_path.split(sep))
            for nominal, real in path_fragments:
                if nominal != real:
                    break
            else:
                if not onloop(path):
                    walk_subdirs[:] = []
                    continue
        # Filter files, if requested
        if file_pattern is not None:
            files = fnmatch.filter(files, file_pattern)
        # We hide the underlying generator's subdirectory list, since we
        # clear it internally when we reach the depth limit (if any)
        if dir_pattern is None:
            subdirs = walk_subdirs[:]
        else:
            subdirs = fnmatch.filter(walk_subdirs, dir_pattern)
        # Report depth
        current_depth = path.count(sep) - initial_depth
        yield WalkedDir(path, subdirs, files, current_depth)
        # Filter directories and implement depth limiting
        if depth is not None and current_depth >= depth:
            walk_subdirs[:] = []
        else:
            walk_subdirs[:] = subdirs

# has_dg = "No"
final_report = open("drmc_dg_report.csv", "wb")
writer = UnicodeWriter(final_report,quoting=csv.QUOTE_ALL)

drmc_filesystem_ID_list = []
tms_report_ID_list = []

writer.writerow(["API and filesystem objectID", "TMS report objectID", "API and filesystem object number", "TMS report object number", "Title", "Creator", "dept", "location on DRMC", "has files", "number of files", "has dg component", "component number"])

skipped_dirs_log = open("drmc_dg_report_log.txt", "w")
skipped_dirs_log.write("Directories excluded from report\n")


# depth should usually be set to 2, but when testing and limiting to one department, set to 1
for info in filter_walk(drmc_path, depth=2):
    if regexp.search(info.path) is not None:
        uni_pwd = info.path
        pwd = uni_pwd.decode("utf-8")
        drmc_obj_id = re.sub('.*---.*---.*---', '', pwd)
        if drmc_obj_id != "":
            TMS_report = csv.reader(open(args.input,"rU"))
            print ("checking "+ drmc_obj_id),
            req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+drmc_obj_id))
            creator = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
            title = req["GetTombstoneDataRestIdResult"]["Title"]
            objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
            APIobjectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
            year = req["GetTombstoneDataRestIdResult"]["Dated"]
            dept = req["GetTombstoneDataRestIdResult"]["Department"]
            print (" / "+ objectnum +"... "),
            recursivefind = subprocess.Popen(["find", pwd, "-type", "f", "-not", "-path", "*/\.*"], stdout=subprocess.PIPE)
            countfiles = subprocess.check_output(["wc", "-l"], stdin=recursivefind.stdout)
            cleanedcount = countfiles.strip()
            yes_rows = [row for row in TMS_report if row[13] == drmc_obj_id]
            for row in yes_rows:
                if cleanedcount != 0:
                    writer.writerow([drmc_obj_id, row[13], objectnum, row[5], title, creator, dept, pwd, "Yes", cleanedcount, "Yes", row[6]])
                    # print "Found component"
                    print
                elif cleanedcount == 0:
                    writer.writerow([drmc_obj_id, row[13], objectnum, row[5], title, creator, dept, pwd, "No", cleanedcount, "Yes", row[6]])
                    print
            if not yes_rows and cleanedcount != 0:
                writer.writerow([drmc_obj_id, "", objectnum, "", title, creator, dept, pwd, "Yes", cleanedcount, "No", ""])
                print cleanedcount+" file(s) without corresponding TMS components     <----------------"
            elif not yes_rows and cleanedcount == 0:
                writer.writerow([drmc_obj_id, "", objectnum, "", title, creator, dept, pwd, "No", cleanedcount, "No", ""])
                print cleanedcount+" file(s) without corresponding TMS components     <----------------"
            drmc_filesystem_ID_list.append(drmc_obj_id)
        else:
            print "drmc_obj_id is none"
            ## write row to "final_report" indicating that dir can not be dealt with programatically due to missing objectID
    else:
        print "Skipping "+ info.path
        skipped_dirs_log.write(info.path+"\n")
        ## write row to "final_report" indicating that dir can not be dealt with programatically due to missing objectID
skipped_dirs_log.close()

TMS_report = csv.reader(open(args.input,"rU"))



x=0

# results when using list, not CSV: 354
firstline = True
for row in TMS_report:
    if firstline: #skip first line
        firstline = False
        continue
    componentID = row[6]
    objectnum = row[5]
    objectid = row[13]
    tms_report_ID_list.append(objectid)
    if objectid != "":
        req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+objectid))
        objectnum = req["GetTombstoneDataRestIdResult"]["ObjectNumber"]
        APIobjectid = req["GetTombstoneDataRestIdResult"]["ObjectID"]
        dept = req["GetTombstoneDataRestIdResult"]["Department"]
        creator = req["GetTombstoneDataRestIdResult"]["AlphaSort"]
        title = req["GetTombstoneDataRestIdResult"]["Title"]

        if objectid in drmc_filesystem_ID_list:
            print objectid +" has a DG and is the repository"
        else:
            print objectid +" has a DG but is not in the repository   <--------------"
            x = x + 1
            writer.writerow(["n/a", objectid, "n/a", objectnum, title, creator, dept, "n/a", "No", "0", "Yes", componentID])
    else:
        print "error - object ID should not be blank, but for "+ objectnum +" it is. Should be here: "+ objectid

print "TMS ID list contains "+str(len(tms_report_ID_list))+" items"
print "DRMC filesystem list contains "+str(len(drmc_filesystem_ID_list))+" items"
print str(x) + " works with DG components, but no files"




