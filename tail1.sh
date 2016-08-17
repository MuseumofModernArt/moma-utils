#!/bin/sh


echo -e '\033[32mPipeline 1: VNX unbaged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail -n 5 /var/log/archivematica/automate-transfer.log && echo -e '\n\n\033[32mPipeline 2: VNX bagged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail -n 5 /usr/lib/archivematica/automation-tools-2/transfers/automate-transfer.log && echo -e '\n\n\033[32mPipeline 3: Standard Isilon workflow >>>>>>>>>>>>>>>>>>>>\033[0m' && tail -n 5 /usr/lib/archivematica/automation-tools-3/transfers/automate-transfer.log