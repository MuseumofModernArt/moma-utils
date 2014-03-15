copy / bag / validate
====================

A utility for copying a specific file or directory from external media, converting the local copy to a Bag named according to repository standards (using MoMA's TMS API), valdating the BagIt generated SHA1 checksums against Hashlib calculated SHA1 of the files on the original source media. Requires [bagit-python], and currently only works with MoMA's TMS API.

[bagit-python]: https://github.com/edsu/bagit

Command Line Usage
------------------

    python pre-ingest.py -i /Volumes/source-drive/source-directory -n "name of transfer" -id 930.2012

Used internally on the MoMA network, this would result in the transfer of the files, and a bag named "Will_Wright---SimCity_2000---930.2012---152406"
  
Arguments
------------------
  - `-id, --accessionid` (required) object/acession number of the artwork.
  - `-i, --input` (required) Full path of the source directory or file
  - `-o, --output` (optional) Full path of the destination. Defaults to Desktop.
  - `-t, --title` (optional) Title of the transfer.
  - `-n, --name` (optional) Name of the person operating the script. This winds up in the Bag's metadata


Output
------------------
Bags are named with the following convention `YYYY-MM-DD_HH:MM:SS__title_of_transfer`

todo: add exception for inability to resolve connection to TMS