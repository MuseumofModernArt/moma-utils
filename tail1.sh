#!/bin/sh


echo -e '\033[32mVNX unbaged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail -n 5 /var/log/archivematica/automate-transfer.log && echo -e '\033[32mVNX bagged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail -n 5 /var/log/archivematica/automate-transfer.log