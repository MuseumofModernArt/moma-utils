#!/usr/bin/env python

# for each folder in target

	# does it adhere to the naming convention?

	# if it is a mezz file (ends with ---mezz)
		# is there a manual normalization folder?
		# does it contain an access folder?
		# does it contain a file with the same name as the file in the /data root?
		# if it passes all these tests continue
		# else report the error and go on to the next folder

	# are all the files present? do a bag verify complete

	# do a bag verify valid

	# if everything has passed, rsync the folder to /staging for bag pipelien

	# after rsync has finished, mv the folder to /ready for ingest