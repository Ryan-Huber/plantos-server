#!/usr/bin/env python

# Our custom utilities functinos
from util import build_mongo_client
# Constants file
from .constants import *
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
# Global variables
_mongo_client = None # We will assign a value to this later

@sensors.route("/")
def select_database():
    return render_template("database_selection.html", databases=DATABASE_NAMES)

@sensors.route("/<database>/")
def select_collection(database):
    if not database in DATABASE_NAMES:
        abort(404)
    colls = COLLECTION_NAMES[database]
    return render_template("collection_selection.html", collections=colls)

@sensors.route("/<database>/<collection>/")
def show_dashboard(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    title = COLLECTION_NAMES[database][collection]
    raw_initial_data = values.find_one(sort=[("date",-1)])
    if (time.time() - raw_initial_data["date"]) > 60:
        initial_data = None
    else:
        initial_data = {}
        for sensor in info.keys():
            if sensor in raw_initial_data:
                initial_data[sensor] = raw_initial_data[sensor]["value"]
            else:
                initial_data[sensor] = 0
    return render_template("dashboard.html", info=info, title=title,
                            initial_data=initial_data, database=database,
                            collection=collection)

@sensors.route("/<database>/<collection>/hour_graphs.html")
def show_hour_graphs(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    return render_template("hour_graphs.html", info=info, database=database,
                            collection=collection)

@sensors.route("/<database>/<collection>/hour_data.json")
def show_hour_data(database, collection):
    after_this_request(add_cache_header)
    values = values_collection(database, collection)
    if not values:
        abort(404)
    sensors = COLLECTION_INFO[database][collection]
    return json.dumps(raw_graphing_data(values,sensors,now()-60*60,now()))

@sensors.route("/<database>/<collection>/day_graphs.html")
def show_day_graphs(database, collection):
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
                            collection=collection, date=date)

@sensors.route("/<database>/<collection>/day_data.json")
def show_day_data(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    _sensors = COLLECTION_INFO[database][collection]
    KEY = "date"
    if not KEY in request.args:
        abort(404)
    date_string = request.args[KEY]
    date = time.strptime(date_string, "%m/%d/%Y")
    date = time.mktime(date)
    if now() < date + 60*60*24: # The day has not ended, generate the data
        after_this_request(add_cache_header)
        return json.dumps(day_graphing_data(values, _sensors, date))
    else: # The day has ended, serve a cached file
        cache_file = day_data_cache_file(database, collection, values, _sensors,
                                        date_string)
        return open(cache_file,'r').read()

@sensors.route("/<database>/<collection>/date_range_graphs.html")
def show_range_graphs(database, collection):
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

@sensors.route("/<database>/<collection>/date_range_data.json")
def show_range_data(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    sensors = COLLECTION_INFO[database][collection]
    KEY1 = "start_date"
    KEY2 = "end_date"
    if not KEY1 in request.args or not KEY2 in request.args:
        abort(404)
    start_date_string = request.args[KEY1]
    end_date_string = request.args[KEY2]
    start_date = datetime.datetime.strptime(start_date_string, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date_string, "%m/%d/%Y")
    def data_gen(start, end):
        curr_date = start
        while curr_date <= end_date:
            curr_date_string = curr_date.strftime("%m/%d/%Y")
            curr_cache_file = day_data_cache_file(database, collection, values,
                                                    sensors, curr_date_string)
            curr_data = json.load(open(curr_cache_file,'r'))
            yield curr_data
            curr_date += datetime.timedelta(1)
    raw_data = []
    num_dates = 0
    for day_data in data_gen(start_date,end_date):
        num_dates += 1
        raw_data.extend(day_data["data"])
    data = []
    for i in range(len(raw_data)/num_dates):
        curr_points = raw_data[num_dates*i:num_dates*(i+1)]
        avg = {}
        for sensor in sensors.keys() + ["date"]:
            vals = [point[sensor] for point in curr_points]
            vals = [val for val in vals if val]
            if len(vals) == 0:
                avg[sensor] = None
            else:
                avg[sensor] = sum(vals)/len(vals)
        data.append(avg)
    return json.dumps({"data": data})

########################
#                      #
#   Helper Functions   #
#                      #
########################
now = time.time
# Returns an mongo client instance. This instance is stored in the _mongo_client
# global variable so that we only have to create it once
def mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = build_mongo_client(current_app)
    return _mongo_client
# Validates the database and collection values received and returns the relevant
# mongo collection of sensor values. If the input is invalid (the database or
# collection doesn't exist, this returns None
def values_collection(database, collection):
    if not database in DATABASE_NAMES:
        return None
    if not collection in COLLECTION_NAMES[database]:
        return None
    return mongo_client()[database][collection]

# Returns a dictionary with all of the data between <ti> and <tf> in the given
# <collection> for the given <sensors>
def raw_graphing_data(values_collection, sensors, ti, tf):
    data = _raw_graphing_data(values_collection, sensors, ti, tf)
    return {"data": data}
def _raw_graphing_data(values_collection, sensors, ti, tf):
    data = []
    points = values_collection.find({"date": {"$gt": ti}}, sort=[("date",1)])
    for raw_point in points:
        if raw_point["date"] > tf:
            break
        point = {sensor: raw_point.get(sensor,{"value":None})["value"]
                for sensor in sensors}
        point["date"] = raw_point["date"]
        data.append(point)
    return data

# Returns a dictionary of values representing all data and stats for the day
def day_graphing_data(values_coll, sensors, date, num_points=1000):
    ti = date
    tf = date + 60*60*24
    data = _graphing_data(values_coll, sensors, ti, tf, num_points)
    stats = _day_stats(values_coll, sensors, ti, tf)
    return {"data": data, "stats": stats}
def _graphing_data(values_coll, sensors, ti, tf, num_points):
    data = []
    duration = float(tf - ti)
    def ranges():
        interval = duration / num_points
        start = ti
        end = ti + interval
        while end <= tf:
            yield (start, end)
            start += interval
            end += interval
    points = values_coll.find({"date": {"$gt": ti}}, sort=[("date",1)])
    try:
        point = points.next()
    except StopIteration:
        return []
    for (start, end) in ranges():
        curr_points = []
        while point["date"] <= end:
            if point["date"] >= start:
                curr_point = {sensor:point.get(sensor,{"value":None})["value"]
                            for sensor in sensors}
                curr_point["date"] = point["date"]
                curr_points.append(curr_point)
            try:
                point = points.next()
            except StopIteration:
                break
        if len(curr_points) == 0:
            avg = {sensor: None for sensor in sensors}
            avg["date"] = (start+end)/2.
        else:
            avg = {"date": (start+end)/2.}
            for sensor in sensors:
                vals = [point[sensor] for point in curr_points]
                vals = [val for val in vals if val]
                if len(vals) == 0:
                    avg[sensor] = None
                else:
                    avg[sensor] = sum(vals)/len(vals)
        data.append(avg)
    return data
def _day_stats(values_coll,  sensors, ti, tf):
    if now() < tf: # The day has not ended
        avg = {sensor: None for sensor in sensors}
        _max = {sensor: None for sensor in sensors}
        _min = {sensor: None for sensor in sensors}
    else: # The day has ended
        day_data = _raw_graphing_data(values_coll, sensors, ti, tf)
        avg = {}
        _max = {}
        _min = {}
        for sensor in sensors:
            vals = [point[sensor] for point in day_data]
            vals = [val for val in vals if val]
            if len(vals) == 0:
                avg[sensor] = None
            else:
                avg[sensor] = sum(vals)/len(vals)
            if len(vals) > 0:
                _max[sensor] = max(vals)
                _min[sensor] = min(vals)
            else:
                _max[sensor] = None
                _min[sensor] = None
    stats = {"date": ti, "averages": avg, "maxima": _max, "minima": _min}
    return stats

# Checks if the day data for <date_string> has already been cached. If not, it
# generates and caches it. Returns the file name for the cached data
def day_data_cache_file(db, coll, values, sensors, date_string):
    date = time.strptime(date_string, "%m/%d/%Y")
    date_string = time.strftime("%m/%d/%Y", date)
    cache_file = "/var/lib/plantos-server/{}/{}/{}.json".format(db,coll,
        date_string.replace("/","_"))
    if not os.path.isfile(cache_file): # No cached file exists
        # Create the containing folder if it doesn't already exist
        dstdir = os.path.dirname(cache_file)
        if not os.path.isdir(dstdir):
            os.makedirs(dstdir)
        date = time.mktime(date)
        print "Generating cache file for {}".format(date_string)
        data = day_graphing_data(values, sensors, date)
        with open(cache_file, 'w+') as f:
            json.dump(data, f)
    return cache_file

# Edits the server response to tell the client not to cache this page
def add_cache_header(response):
    response.headers['Cache-Control'] = 'public,max-age=0,no-cache'
    return response
