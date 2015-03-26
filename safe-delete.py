#!/usr/bin/env python

# The purpose of this script is to provide a report of what transfers
# have been sucsesfully processed by Archivematica's automation-tools,
# so that the original source of the transfer may be deleted since the
# materials are safely packaged and stored in an AIP.
#
# This mission is accomplished by looking at the sqlite database
# maintained by Archivematica's automation-tools, and talk to
# the Binder API in order to ensure that if automation-tools says
# it has processed an AIP, that this AIP has actually been 100%
# sucsesfully processed and is tracked in Binder.
# 
# This is necesary because if an automated transfer fails at any
# point in the workflow (for instance, normalization, or AIP storage),
# automation-tools is ignorant of this fact.

# What follows is some pseudo-code...

open csv for writing
open anothercsv for writing and reading

for row in sqliteDB:
	read UUID of transfer
	ping Binder API with UUID of transfer (AIP will have same UUID)
	if Binder responds saying that it has this AIP:
		write row in csv with UUID, and construct the theoretical path to the transfer source to be deleted
	else:
		write row in anothercsv with UUID
		delete this row from sqliteDB

