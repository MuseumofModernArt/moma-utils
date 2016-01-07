#!/bin/sh


#### portrait
tmux new-session -d -s foo 'htop'
tmux rename-window 'Foo'
tmux select-window -t foo:0
tmux split-window -v 'tail -f /var/log/archivematica/automate-transfer.log'
tmux resize-pane -U 28
tmux split-window -v 'man top'
tmux resize-pane -U 15
tmux split-window -v 'watch -n100 df -h'
tmux resize-pane -U 15
# tmux set -g pane-border-style fg=black
# tmux set -g pane-active-border-style fg=black
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