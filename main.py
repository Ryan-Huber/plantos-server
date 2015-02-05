#!/usr/bin/env python

# Constants file
from sensors.constants import DATABASE_NAMES
from sensors.constants import COLLECTION_NAMES
from sensors.constants import COLLECTION_INFO
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
# PyMongo setup
from pymongo import MongoClient
flask_app.mongo_client = MongoClient(flask_app.config["HOST_IP"])
username = flask_app.config["MONGO_USERNAME"]
password = flask_app.config["MONGO_PASSWORD"]
try:
    flask_app.mongo_client.admin.authenticate(username, password)
except:
    print """Failed to authenticate to database. Either the database does not
    require authentication or the login information in instance application.cfg
    is incorrect"""
# Mongoengine setup
from flask.ext.mongoengine import MongoEngine
flask_app.mongoengine = MongoEngine(flask_app)
# Register Blueprints
from plants import bp as plants_bp
flask_app.register_blueprint(plants_bp)
from sensors.main import sensors
flask_app.register_blueprint(sensors)
# SocketIO Setup
from flask.ext.socketio import SocketIO
socketio = SocketIO(flask_app)
# Authentication
from flask.ext.basicauth import BasicAuth
basic_auth = BasicAuth(flask_app)

# Register sensor board web management blueprint
import sys
sys.path.append("./sensor-board")
from web_management.server import bp as board_management_blueprint
flask_app.register_blueprint(board_management_blueprint, url_prefix="/manage")

@flask_app.route("/")
def index():
    return render_template("index.html")

# A background thread that emits new data points to clients from the specified
# collection as they arrive
def background_thread(system, board):
    values = flask_app.mongo_client[system][board]
    namespace = "/{}/{}/data".format(system,board)
    sensors = COLLECTION_INFO[system][board]
    count = values.count()
    while True:
        new_count = values.count()
        if new_count > count:
            try:
                count = new_count
                raw_point = values.find_one(sort=[("date",-1)])
                point = {sensor:raw_point[sensor]["value"] for sensor in sensors}
                point["date"] = raw_point["date"]
                socketio.emit('data', json.dumps(point), namespace=namespace)
            except KeyError:
                print "Invalid point received in {}, {}".format(system, board)
                if point or raw_point:
                    print point or raw_point
        time.sleep(1)

def run_server(*args):
    for system in DATABASE_NAMES.keys():
        for collection in COLLECTION_NAMES[system].keys():
            # Start a thread to monitor the collection
            thread = Thread(target=background_thread, args=(system, collection))
            thread.daemon = True
            print "Starting thread {} : {}".format(system, collection)
            thread.start()
            print "Started thread {} : {}".format(system, collection)
            # Make a socketio connect callback for the data namespace
            namespace = "/{}/{}/data".format(system, collection)
            socketio.on('connect', namespace=namespace)(lambda:None)
    if flask_app.debug:
        socketio.run(flask_app, host='0.0.0.0', port=8080)
    else:
        socketio.run(flask_app, host='0.0.0.0', port=80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CityFARM web server")
    parser.add_argument("-d", "--debug", action="store_true", help="enable\
            flask debug mode")
    args = parser.parse_args()
    flask_app.debug = args.debug
    run_server()
