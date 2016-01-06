#!/bin/sh

tmux new-session -d -s foo 'htop'
tmux rename-window 'Foo'
tmux select-window -t foo:0
tmux split-window -v 'tail -f /var/log/archivematica/automate-transfer.log'
tmux resize-pane -U 5
tmux split-window -v 'tail -f /var/log/archivematica/automate-transfer.log' #this will be atom worker log on vrmdrmcatom
tmux resize-pane -R 23
tmux select-pane -t 1
tmux split-window -v 'tail -f /var/log/archivematica/automate-transfer.log' #this will be second automation-tools log
tmux select-pane -t 1 
tmux split-window -v 'df -h'
tmux select-pane -t 0
tmux resize-pane -U 2
tmux -2 attach-session -t foo
