#!/usr/bin/env python

# Our custom utilities functions
from util import *
# Constants file
from sensors.constants import *
# General imports
import os
import time
import json
import shutil
import argparse
import gevent.monkey
gevent.monkey.patch_thread()
from threading import Thread
# Flask Setup
from flask import Flask
from flask import render_template
flask_app = Flask(__name__, instance_relative_config = True)
config_file_path = os.path.join(flask_app.instance_path, "application.cfg")
if not os.path.isfile(config_file_path):
    print """Copying example configuration file. These settings will probably
    not work. Please edit the configuration file in instance/application.cfg
    and provide actual values"""
    example_cfg = os.path.join(flask_app.root_path, "application.cfg.example")
    if not os.path.isfile(example_cfg):
        raise Exception("Example configuration file not found")
    if not os.path.isdir(flask_app.instance_path):
        os.makedirs(flask_app.instance_path)
    shutil.copyfile(example_cfg, config_file_path)

flask_app.config.from_pyfile("application.cfg")
# Register Blueprints
from plants.main import plants
flask_app.register_blueprint(plants)
from sensors.main import sensors
flask_app.register_blueprint(sensors)
# SocketIO Setup
from flask.ext.socketio import SocketIO
socketio = SocketIO(flask_app)
# Global variables
mongo_client = None # We will assign a value to this later

@flask_app.route("/")
def main_page():
    return render_template("index.html")

# A background thread that emits new data points to clients from the specified
# collection as they arrive
def background_thread(system, board):
    values = mongo_client[system][board]
    namespace = "/{}/{}/data".format(system,board)
    sensors = COLLECTION_INFO[system][board]
    count = values.count()
    while True:
        new_count = values.count()
        if new_count > count:
            try:
                count = new_count
                raw_point = values.find_one(sort=[("date",-1)])
                point={sensor:raw_point[sensor]["value"] for sensor in sensors}
                point["date"] = raw_point["date"]
                socketio.emit('data', json.dumps(point), namespace=namespace)
            except KeyError:
                print "Invalid point received in {}, {}".format(system, board)
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CityFARM web server")
    parser.add_argument("-d", "--debug", action="store_true", help="enable\
            flask debug mode")
    args = parser.parse_args()
    flask_app.debug = args.debug
    mongo_client = build_mongo_client(flask_app)
    for system in DATABASE_NAMES.keys():
        for collection in COLLECTION_NAMES[system].keys():
            # Start a thread to monitor the collection
            thread = Thread(target=background_thread, args=(system, collection))
            thread.daemon = True
            thread.start()
            # Make a socketio connect callback for the data namespace
            namespace = "/{}/{}/data".format(system, collection)
            socketio.on('connect', namespace=namespace)(lambda:None)
    if args.debug:
        socketio.run(flask_app, host='0.0.0.0')
    else:
        socketio.run(flask_app, host='0.0.0.0', port=80)
