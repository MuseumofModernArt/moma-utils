import csv
import os
from cStringIO import StringIO

## variables
asset_path = '/home/archivesuser/drmc_dam_bulk/Assets/'
csv_path = '/home/archivesuser/drmc_dam_bulk/CSV/metadata.csv'
extensions_to_remove = ['.txt', '.smil', '.md5', '.DVC']
list_of_files_to_rm = []

for root, dirs, files in os.walk(asset_path):
	for file in files:
		if file.endswith(tuple(extensions_to_remove)):
			list_of_files_to_rm.append(file)
			os.remove(asset_path+file)

with open('out.csv', 'wb') as out_f:
	out = csv.writer(out_f, delimiter=',')
	with open(csv_path, 'rb') as f:
		for row in csv.reader(f, delimiter=','):
			if row[0] not in list_of_files_to_rm:
				out.writerow(row)

os.remove(csv_path)
os.rename('out.csv', csv_path)