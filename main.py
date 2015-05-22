#!/usr/bin/env python

# Constants file
from sensors.constants import DATABASE_NAMES
from sensors.constants import COLLECTION_NAMES
from sensors.constants import COLLECTION_INFO
from sensors.constants import TRAY_LIST
from sensors.constants import TRAY_SENSORS
from sensors.constants import WATER_SENSOR_BOARDS
from sensors.constants import SYSTEM_URLS
# dummyData file
from dummyData import traySelectQuery
from dummyData import trayQuery
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
from flask import redirect, url_for, abort
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
# Custom Werkzeug converter
from werkzeug.routing import BaseConverter
class NoStaticConverter(BaseConverter):
    def __init__(self, url_map):
        super(NoStaticConverter, self).__init__(url_map)
        self.regex='((?!static)[^/])*'
flask_app.url_map.converters['no_static'] = NoStaticConverter
# Register Sensor Blueprint
from sensors.main import sensors
flask_app.register_blueprint(sensors)
# Authentication
from flask.ext.basicauth import BasicAuth
basic_auth = BasicAuth(flask_app)

from collections import defaultdict
trayPlantDict = defaultdict(list)
plantImages = []

@flask_app.route("/")
def index():
    return render_template("index.html", databases=DATABASE_NAMES)

@flask_app.route("/<system>/")
def traySelect(system):
    if not system in TRAY_LIST:
        abort(404)
    systemUrl = SYSTEM_URLS[system]
    return render_template("trayselect3d.html", databases=DATABASE_NAMES, current_database=system, sysUrl=systemUrl)

@flask_app.route("/<system>/tray/<int:traynum>")
def trayView(system, traynum):
    if not system in TRAY_LIST:
        abort(404)
    '''if traynum > len(TRAY_LIST[system]):
        abort(404)
    tray = TRAY_LIST[system][max(traynum-1, 0)]
    trayString = str(system) + "_" + str((traynum-1))
    plants = trayPlantDict[trayString]
    locs = []
    for plant in plants:
        ip = plant["ip"].split('.')
        x = int(ip[3])+1
        y = int(ip[4])+1
        locs.append([x,y])
    if system == "main_system":
        sensor_info = COLLECTION_INFO[system][TRAY_SENSORS[traynum-1]]
    else:
        sensor_info = {}
    board_id = WATER_SENSOR_BOARDS[TRAY_SENSORS[traynum-1]]
    '''

    return render_template("trayView3d.html", 
            databases=DATABASE_NAMES,
            current_database=system, 
            #tray=tray, 
            #plants=plants, 
            #plantImages=plantImages,
            #plantLocations=locs, 
            #sensor_info=sensor_info, 
            #board_id=board_id,
            queryData = trayQuery
            )

##### Testing for New Backend APIs #####


@flask_app.route("/Testing/test1")
def traySelectTest():
    queryData = trayQuery
    return render_template("TestingTrayView3d.html", databases=DATABASE_NAMES, queryData=queryData)



import csv
def plantImgsFromCSV(fileString):
    f = open(fileString, 'rU')
    csv_f = csv.DictReader(f)
    for plant in csv_f:
        plantImages.append(plant)


def parseCSV(fileString):
    f = open(fileString, 'rU')
    csv_f = csv.DictReader(f)
    for plant in csv_f:
        ip = plant["ip"]
        if ip == "" or ip == "Discarded ":
            continue
        ip = ip.split('.')

        if ip[0] == "1":#Main system
            if ip[1]=="0":#Bay 0
                if ip[2]=="0":
                    trayPlantDict["main_system_0"].append(plant)

            elif ip[1]=="1":#Bay1
                if ip[2]=="0":
                    trayPlantDict["main_system_1"].append(plant)
                elif ip[2]=="1":
                    trayPlantDict["main_system_2"].append(plant)
                elif ip[2]=="2":
                    trayPlantDict["main_system_3"].append(plant)

            elif ip[1]=="2":#Bay2
                if ip[2]=="0":
                    trayPlantDict["main_system_4"].append(plant)
                elif ip[2]=="1":
                    trayPlantDict["main_system_5"].append(plant)

            elif ip[1]=="3":#Bay3
                if ip[2]=="0":
                    trayPlantDict["main_system_6"].append(plant)
                elif ip[2]=="1":
                    trayPlantDict["main_system_7"].append(plant)

            elif ip[1]=="4":#Bay4
                if ip[2]=="0":
                    trayPlantDict["main_system_8"].append(plant)

            #pass #go to a main sys tray
        elif ip[0] == "2":
            trayPlantDict["groBot_0"].append(plant) #go to groBot1Trayy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CityFARM web server")
    parser.add_argument("-d", "--debug", action="store_true", help="enable\
            flask debug mode")
    args = parser.parse_args()
    flask_app.debug = args.debug
    parseCSV("static/PlantData.csv")
    plantImgsFromCSV("static/plantImgCSV.csv")
    flask_app.run(use_debugger=True, use_reloader=False)
