#!/bin/sh

# creates a tmux layout for monitoring MoMA's automated ingest in Archivematica

tmux new-session -d -s vert 'htop'
tmux rename-window 'vert'
tmux select-window -t vert:0
tmux split-window -v ""watch --color -n 1 "echo '\033[32mVNX unbaged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail /var/log│5c37be84-13d0-456b-93f6-f596e53cd7ff-49.2015.10.pdf,188734
/archivematica/automate-transfer.log""

tmux split-window -v 'watch --color -n 1 "echo '\033[32mVNX baged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail /var/log│5c37be84-13d0-456b-93f6-f596e53cd7ff-49.2015.10.pdf,188734
/archivematica/automate-transfer.log"'

tmux split-window -v 'watch --color -n 1 "echo '\033[32mIsilon bagged >>>>>>>>>>>>>>>>>>>>\033[0m' && tail /var/log│5c37be84-13d0-456b-93f6-f596e53cd7ff-49.2015.10.pdf,188734
/archivematica/automate-transfer.log"'

tmux split-window -v -t 1 'watch -n 1 "ls -lh ~/drmc_dam_bulk/Assets/ | wc -l && du -h ~/drmc_dam_bulk/Assets/"'
tmux split-window -v -t 3 'watch -n 1 tail ~/drmc_dam_bulk/CSV/metadata.csv'
tmux -2 attach-session -t vert


