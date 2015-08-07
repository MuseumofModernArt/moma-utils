#!/bin/bash

clear

echo "about to sync dam files... here is a list of pre-sanitized files"
ls /home/archivesuser/drmc_dam_bulk/Assets/
echo "running python script for removal of bad files"
python /home/archivesuser/moma-utils/dam-sync/dam_cleanup.py
echo "here is the cleaned up list"
ls /home/archivesuser/drmc_dam_bulk/Assets/

echo "syncing DAM files..."

mv /home/archivesuser/drmc_dam_bulk/Assets/* /home/archivesuser/dam02_watch

echo "done syncing files to DAM watched dir... here is the file listing of the DAM watched dir"
ls /home/archivesuser/dam02_watch
