#!/bin/bash

clear

echo "syncing DAM files..."

mv /home/archivesuser/drmc_dam_bulk/Assets/* /home/archivesuser/dam_watched_sync/WatchFolder
cp /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/drmc_dam_bulk/csvbackups/$(date -d "today" +"%Y%m%d%H%M").metadata.csv
mv /home/archivesuser/drmc_dam_bulk/CSV/metadata.csv /home/archivesuser/dam_watched_sync/CSV

echo "done"