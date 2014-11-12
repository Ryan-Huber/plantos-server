#!/bin/bash
uwsgi --socket /tmp/uwsgi.sock --wsgi-file main.py --callable flask_app --processes 4 --threads 2 --stats 127.0.0.1:9191
