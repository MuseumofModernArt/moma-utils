#!/bin/bash

clear

echo "syncing DAM CSV..."
echo "here is the CSV contents"
cat /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv
echo "making backup of CSV"
cp /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/drmc_dam_bulk/csvbackups/$(date -d "today" +"%Y%m%d%H%M").metadata.csv
echo "moving metadata.csv to DAM sync dir"
mv /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/DRMC_DAM/CSV
echo "listing CSV watch folder after mv"
ls /home/archivesuser/DRMC_DAM/CSV
echo "Done!"
