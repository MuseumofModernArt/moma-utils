#!/usr/bin/tmux source-file

new-session -d
split-window -d -t 0 -v
split-window -d -t 0 -h
split-window -d -t 0 -v
split-window -d -t 2 -v

send-keys -t 0 'htop' enter

send-keys -t 1 'htop' enter C-l

send-keys -t 2 'htop' enter

send-keys -t 3 'htop' enter

## Just a convenience shell
send-keys -t 4 'htop' enter C-l
select-pane -t 4

attach