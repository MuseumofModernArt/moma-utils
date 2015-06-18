#!/bin/sh

tmux new-session -d -s foo 'htop'
tmux rename-window 'Foo'
tmux select-window -t foo:0
tmux split-window -h 'tail -f /var/log/archivematica/automate-transfer.log'
tmux split-window -v -t 0 ''
tmux split-window -v -t 1 'watch -n 1 "ls -lh ~/drmc_dam_bulk/Assets/ | wc -l && du -h ~/drmc_dam_bulk/Assets/"'
tmux split-window -v -t 3 'watch -n 1 tail ~/drmc_dam_bulk/CSV/metadata.csv'
tmux -2 attach-session -t foo
