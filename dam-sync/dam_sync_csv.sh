#!/bin/bash

LOGFILE=/home/archivesuser/drmc_dam_bulk/csvbackups/$(date -d "today" +"%Y%m%d%H%M").metadata.log

echo "`date +%H:%M:%S : Starting work" >> $LOGFILE

clear

echo "syncing DAM CSV..." >> $LOGFILE

cp /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/drmc_dam_bulk/csvbackups/$(date -d "today" +"%Y%m%d%H%M").metadata.csv
# mv /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/dam_watched_sync
mv /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/drmc_dam_bulk/staging/CSV

echo "listing CSV watch folder after mv"

ls /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/dam_watched_sync/CSV >> $LOGFILE

echo "Done!" >> $LOGFILE

mail -s "DRMC metadata available" -t jennifer_sellar@moma.org, david_garfinkel@moma.org, ben_fino-radin@moma.org <<< "New DRMC metadata has just been synced..."