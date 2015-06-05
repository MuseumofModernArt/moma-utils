#!/bin/bash

clear

echo "syncing DAM files..."

mv /home/archivesuser/drmc_dam_bulk/Assets/* /home/archivesuser/dam_watched_sync/WatchFolder

echo "done"

mail -s "DRMC assets available" -t jennifer_sellar@moma.org, david_garfinkel@moma.org, ben_fino-radin@moma.org <<< "New DRMC assets have just been synced..."