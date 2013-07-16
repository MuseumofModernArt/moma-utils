copy / bag / validate
====================

A utility for copying a specific file or directory from external media, converting the local copy to a Bag, and then valdating the BagIt generated MD5 checksums against Hashlib generated MD5s of the files on the original source media.

Command Line Usage
------------------

    python pre-ingest.py -i /Volumes/source-drive/source-directory -n "name of transfer"
  
Arguments
------------------
  - `-i, --input` (required) Full path of the source directory or file
  - `-o, --output` (optional) Full path of the destination. Defaults to Desktop.
  - `-t, --title` (optional) Title of the transfer.
  - `-n, --name` (optional) Name of the person operating the script. This winds up in the Bag's metadata


Output
------------------
Bags are named with the following convention `YYYY-MM-DD_HH:MM:SS__title_of_transfer`
