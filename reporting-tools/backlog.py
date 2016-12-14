#!/usr/bin/env python

import argparse
import os
import json
import urllib2
import ast

parser = argparse.ArgumentParser(description="script for reporting on the 'artwork level' backlog")
parser.add_argument('-i', '--input', type=str, required=True, help='target directory')
args = parser.parse_args()

ComponentNameKeywords = ['digital', 'file', 'MOV']

DGcounter = 0
ComponentCounter = 0
keywordCounter = 0
artworkCounter = 0

artworkDGCounter = 0

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

for path in get_immediate_subdirectories(args.input):
	# print path
	parts = path_parts = path.split('---')
	# print parts
	if len(parts) == 4:
		artworkCounter = artworkCounter + 1
		idnum = parts[3]
		print "--------------------------"
		print path
		try:
			switch = False
			req = json.load(urllib2.urlopen("http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetTombstoneDataRest/ObjectID/"+idnum))
			components = req["GetTombstoneDataRestIdResult"]["Components"]
			components = ast.literal_eval(components)
			for component in components:
				
				ComponentCounter = ComponentCounter + 1
				if 'DG' in component['ComponentNumber'] and switch is False:
					# print "found a DG in "+idnum
					DGcounter = DGcounter + 1
					switch = True
				else:					
					componentID = str(component['ComponentID'])
					component_url = "http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetComponentDetails/Component/"+componentID
					component_request = json.load(urllib2.urlopen(component_url))
					componentName = component_request["GetComponentDetailsResult"]["ComponentName"]
					for keyword in ComponentNameKeywords:
						if keyword in componentName and switch is False:
							# print "found keyword in component name"
							print keyword+" found in "+componentName+str(component['ComponentNumber'])
							keywordCounter = keywordCounter + 1
							switch = True

							### right now this is counting multiple keywords per component, need to set it to continue to next component after one is found
				

			# print req
		except urllib2.HTTPError, err:
			print err
		print "--------------------------\n\n"
	else:
		print "improperly named dir"
		print path

	print "Out of "+str(artworkCounter)+" artworks, there are "+str(ComponentCounter)+" components, and "+str(DGcounter)+" are DG, and "+str(keywordCounter)+" have matching keywords"
	# print "Found "+str(DGcounter)+" DG components out of "+str(ComponentCounter)+" components in the backlog"
	# print "Found "+str(keywordCounter)+" components with matching keywords our of "+str(ComponentCounter)+" components in the backlog"


############################# pasted in component stuf
# components = object_request['Components']
# components = ast.literal_eval(components)


# component_url = "http://vmsqlsvcs.museum.moma.org/TMSAPI/TmsObjectSvc/TmsObjects.svc/GetComponentDetails/Component/"+componentID
# component_request = json.load(urllib2.urlopen(component_url))

# componentName = component_request["GetComponentDetailsResult"]["ComponentName"]
# componentNumber = component_request["GetComponentDetailsResult"]["ComponentNumber"]
# componentID = component_request["GetComponentDetailsResult"]["ComponentID"]
# Attributes = component_request["GetComponentDetailsResult"]["Attributes"]
