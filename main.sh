#!/bin/bash
uwsgi --socket /tmp/uwsgi.sock --wsgi-file main.py --callable run_server \
--processes 1 --threads 1 --stats 127.0.0.1:9191
