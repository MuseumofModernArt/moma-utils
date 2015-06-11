#!/usr/bin/tmux source-file

new-session -d
split-window -d -t 0 -v
split-window -d -t 0 -h
split-window -d -t 0 -v
split-window -d -t 2 -v

send-keys -t 0 'workon my_virtualenv' enter C-l
send-keys -t 0 'python manage.py runserver' enter

send-keys -t 1 'htop' enter C-l

send-keys -t 2 'workon my_virtualenv' enter C-l
send-keys -t 2 'python manage.py celery worker --loglevel=info' enter

send-keys -t 3 'workon my_virtualenv' enter C-l
send-keys -t 3 'cd MyProject/webui/' enter
send-keys -t 3 'brunch watch' enter

## Just a convenience shell
send-keys -t 4 'workon my_virtualenv' enter C-l
select-pane -t 4

attach