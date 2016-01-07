#!/bin/sh


#### portrait
tmux new-session -d -s foo 'htop'
tmux rename-window 'Foo'
tmux select-window -t foo:0
tmux set-window-option remain-on-exit on
tmux split-window -v 'watch -n1 "echo 'test' && tail -f /var/log/archivematica/automate-transfer.log"'
tmux resize-pane -U 28
tmux split-window -v 'tail -f /var/log/archivematica/automate-transfer.log'
tmux resize-pane -U 28
tmux split-window -v 'watch -n100 df -h'
tmux resize-pane -U 22
tmux split-window -v "watch -n100000 df -h"
tmux resize-pane -U 18
tmux split-window -v 'watch -n100 ls /home/archivesuser'
tmux select-pane -t 3
tmux split-window -h 'echo 'nothing goes here''
tmux resize-pane -L 25
tmux select-pane -t 6
tmux resize-pane -U 6
tmux split-window -h 'watch -n100 ls /home/archivesuser/dam02'
tmux resize-pane -R 26
tmux set -g pane-border-style fg=black
tmux set -g pane-active-border-style fg=black
tmux -2 attach-session -t foo




#### landscape

# tmux new-session -d -s foo 'htop'
# tmux rename-window 'Foo'
# tmux select-window -t foo:0
# tmux split-window -v 'watch -n1 bash part2.sh'
# tmux split-window -h 'top'
# tmux resize-pane -U 10
# tmux resize-pane -R 25
# tmux select-pane -t 1
# tmux split-window -v 'man top'
# tmux resize-pane -U 10
# tmux split-window -v 'watch -n100 df -h' #disk monitoring
# tmux resize-pane -U 5
# tmux -2 attach-session -t foo
# tmux set -g pane-border-style fg=black
# tmux set -g pane-active-border-style fg=black