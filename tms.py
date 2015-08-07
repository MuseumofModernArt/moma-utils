#!/usr/bin/env python

import csv, argparse, urllib2, json, ast

parser = argparse.ArgumentParser(description="script for adding TMS metadata to a transfer, uses the Archivemitca metadata.csv format")
parser.add_argument('-i', '--input', type=str, required=True, help='path to transfer you want to add metadata for.')
args = parser.parse_args()

dirname = args.input
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

Attributes = ast.literal_eval(Attributes)

# look to see if the media label created date exists
for start_item in Attributes:
	item = ast.literal_eval(start_item)
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

elementList = [dc_ident1, dc_ident2, dc_title, dc_creator, dc_date, dc_format1, dc_format2, componentName, componentNumber,
				componentID, componentDate, componentChannels, componentCopyinSet, componentStatus, componentFormat]

print elementList

# find out what elements it has in TMS
# write header of csv accordingly

# for file in /data dir of transfer:
# 	write filename
# 	write elements