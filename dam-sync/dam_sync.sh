#!/bin/bash

clear

echo "running python script for removal of bad files"

python dam_cleanup.py

echo "syncing DAM files..."

mv /home/archivesuser/drmc_dam_bulk/Assets/* /home/archivesuser/home/archivesuser/dam02_watch

echo "done"

mail -s "DRMC assets available" -t jennifer_sellar@moma.org, david_garfinkel@moma.org, ben_fino-radin@moma.org <<< "New DRMC assets have just been synced..."