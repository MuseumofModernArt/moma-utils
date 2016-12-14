#!/usr/bin/env python

import csv, argparse, urllib2, json, ast, os, sys

parser = argparse.ArgumentParser(description="script for adding TMS metadata to a transfer, uses the Archivemitca metadata.csv format")
parser.add_argument('-i', '--input', type=str, required=True, help='path to transfer you want to add metadata for.')
parser.add_argument('-o', '--output', type=str, required=True, help='where to put csv')
args = parser.parse_args()

dirname = os.path.basename(os.path.normpath(args.input))
objectID = dirname.split('---')[2]
componentID = dirname.split('---')[1]

# get the object metadata
object_url = "http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+objectID
object_request = json.load(urllib2.urlopen(object_url))

# get the component metadata
component_url = "http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetComponentDetails/Component/"+componentID
component_request = json.load(urllib2.urlopen(component_url))

# put object metdata in its place
dc_ident1 = object_request["GetTombstoneDataRestIdResult"]["ObjectID"]
dc_ident2 = object_request["GetTombstoneDataRestIdResult"]["ObjectNumber"]
dc_title = object_request["GetTombstoneDataRestIdResult"]["Title"]
dc_creator = object_request["GetTombstoneDataRestIdResult"]["DisplayName"]
dc_date = object_request["GetTombstoneDataRestIdResult"]["Dated"]
dc_format1 = object_request["GetTombstoneDataRestIdResult"]["Classification"]
dc_format2 = object_request["GetTombstoneDataRestIdResult"]["Medium"]

# put component metadata in its place
componentName = component_request["GetComponentDetailsResult"]["ComponentName"]
componentNumber = component_request["GetComponentDetailsResult"]["ComponentNumber"]
componentID = component_request["GetComponentDetailsResult"]["ComponentID"]
Attributes = component_request["GetComponentDetailsResult"]["Attributes"]

#initialize component variables
componentStatus = ""
componentFormat = ""

try:
	Attributes = ast.literal_eval(Attributes)
except SyntaxError:
	print "Caught a SyntaxError: "+str(sys.exc_info())
except ValueError:
	print "Caught a ValueError: "+str(sys.exc_info())

componentDate = ''
componentChannels = ''
componentCopyinSet = ''

# look to see if the media label created date exists
for item in Attributes:
	# print start_item
	# item = ast.parse(start_item, mode='eval')
	try:
		if item['Media Label'] == 'Created Date':
			componentDate = item['Remarks']
		if item['Media Label'] == 'Channels':
			componentChannels = item['Remarks']
		if item['Media Label'] == 'Copy in set':
			componentCopyinSet = item['Remarks']
		componentStatus = item['Status']
		componentFormat = item['Media Format']	
	except KeyError:
		print "nada"

 



# it doesn't matter if the given component doesn't have all of the elements in the CSV header - they'll just be ommitted in the XML - not blank
c = csv.writer(open(args.output, "wb"))
c.writerow(["filename","dc.identifier","dc.identifier","dc.title","dc.creator","dc.date","dc.format","dc.format","componentName",
			"componentNumber","componentID","createdDate","channels","copyInSet","status","relation","textEntry"])


# for file in /data dir of transfer:
# 	write filename
# 	write elements

for filename in os.listdir(args.input+'/data'):
	elementList = [filename,dc_ident1, dc_ident2, dc_title, dc_creator, dc_date, dc_format1, dc_format2, componentName, componentNumber,
					componentID, componentDate, componentChannels, componentCopyinSet, componentStatus, componentFormat]

	c.writerow(elementList)