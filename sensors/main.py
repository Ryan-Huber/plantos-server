#!/usr/bin/env python

# Constants file
from .constants import DATABASE_NAMES
from .constants import COLLECTION_NAMES
from .constants import COLLECTION_INFO
from .constants import WATER_SENSOR_BOARDS
# General imports
import os
import time
import json
import os.path
import datetime
# Flask setup
from flask import abort
from flask import request
from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import after_this_request
sensors = Blueprint('sensors', __name__, static_folder="static",
                    template_folder="templates", url_prefix="/sensors")

@sensors.route("/")
def select_database():
    return render_template("database_selection.html", databases=DATABASE_NAMES)

@sensors.route("/<database>")
def select_sensetype(database):
    if not database in DATABASE_NAMES:
        abort(404)
    return render_template("sensetype_selection.html", databases=DATABASE_NAMES,
            current_database=database)

@sensors.route("/<database>/<sensetype>")
def select_collection(database, sensetype):
    if not database in DATABASE_NAMES:
        abort(404)
    colls = COLLECTION_NAMES[database]
    if not sensetype.lower() in ["water", "atmospheric"]:
        abort(404)
    return render_template("sensor_base_page.html", current_database=database,
            databases=DATABASE_NAMES, collections=colls, sensor_type=sensetype)

@sensors.route("/<database>/<sensetype>/<collection>/")
def show_dashboard(database, sensetype, collection):
    info = COLLECTION_INFO[database][collection]
    title = COLLECTION_NAMES[database][collection]
    board_id = WATER_SENSOR_BOARDS[collection]
    return render_template("dashboard.html", info=info, title=title,
            database=database, collection=collection, databases=DATABASE_NAMES,
            board_id=board_id)

@sensors.route("/<database>/<sensetype>/<collection>/hour_graphs.html")
def show_hour_graphs(database, sensetype, collection):
    info = COLLECTION_INFO[database][collection]
    return render_template("hour_graphs.html", info=info, database=database,
                            collection=collection, databases=DATABASE_NAMES)

@sensors.route("/<database>/<sensetype>/<collection>/day_graphs.html")
def show_day_graphs(database, sensetype, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    KEY = "date"
    if KEY in request.args:
        date = request.args[KEY]
    else:
        date = time.strftime("%m/%d/%Y")
    return render_template("day_graphs.html", info=info, database=database,
                            collection=collection, date=date, databases=DATABASE_NAMES)

@sensors.route("/<database>/<sensetype>/<collection>/date_range_graphs.html")
def show_range_graphs(database, sensetype, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    KEY1 = "start_date"
    KEY2 = "end_date"
    if not KEY1 in request.args or not KEY2 in request.args:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    start_date = request.args[KEY1]
    end_date = request.args[KEY2]
    return render_template("date_range_graphs.html", database=database,
                            collection=collection, start_date=start_date,
                            end_date=end_date, info=info)
