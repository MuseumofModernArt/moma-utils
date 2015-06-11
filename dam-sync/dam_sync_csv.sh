#!/bin/bash

clear

echo "syncing DAM CSV..."

cp /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/drmc_dam_bulk/csvbackups/$(date -d "today" +"%Y%m%d%H%M").metadata.csv
mv /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/DRMC_DAM/CSV

echo "listing CSV watch folder after mv"

echo "Done!"

mail -s "DRMC metadata available" -t jennifer_sellar@moma.org, david_garfinkel@moma.org, ben_fino-radin@moma.org <<< "New DRMC metadata has just been synced..."