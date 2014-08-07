#!/usr/bin/env python

# General includes
import sys
import time
import json
import datetime
import gevent.monkey
from os.path import isfile
gevent.monkey.patch_thread()
from threading import Thread
# Flask setup
from flask import Flask
from flask import abort
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template
from flask import after_this_request
from flask.ext.socketio import SocketIO
flask_app = Flask(__name__)
flask_app.config['DEBUG'] = True
socketio = SocketIO(flask_app)
# PyMongo setup
from pymongo import MongoClient
client = MongoClient()
with open("./database_credentials.txt","r") as f:
    (username,password) = f.readline()[:-1].split(",")
client.admin.authenticate(username,password)
# Our site-specific constants
from constants import *

@flask_app.route("/")
def select_database():
    return render_template("database_selection.html", databases=DATABASE_NAMES)

@flask_app.route("/plants")
def browse_plants():
    return render_template("plants.html")

@flask_app.route("/plants.json")
def show_plants():
    plants = []
    for plant in client.plants.plants.find(sort=[("id",1)]):
        plant.pop("_id")
        plant_type = client.plants.plant_types.find_one({"_id":plant["type"]})
        plant_type.pop("_id")
        plant["type"] = plant_type
        plants.append(plant)
    if "type" in request.args:
        _type = request.args["type"]
        plants = [p for p in plants if p["type"]["common_name"] == _type]
    return json.dumps(plants)

@flask_app.route("/plants/by-id/new.html", methods=['GET','POST'])
def new_plant():
    if request.method == 'GET':
        return render_template("new_plant.html")
    else:
        plant = parse_form(request.form)
        _type = client.plants.plant_types.find_one({"common_name":plant["type"]})
        if _type is None:
            abort(500)
        plant["type"] = _type["_id"]
        client.plants.plants.insert(plant)
        return redirect("/plants")

@flask_app.route("/plants/by-id/<_id>")
def show_plant(_id):
    plant = client.plants.plants.find_one({"id":_id})
    if plant is None:
        abort(404)
    plant.pop("_id")
    plant_type = client.plants.plant_types.find_one({"_id":plant["type"]})
    plant_type.pop("_id")
    plant["type"] = plant_type
    return render_template("view_plant.html", plant=plant)

@flask_app.route("/plants/by-id/<_id>/edit.html", methods=['GET','POST'])
def edit_plant(_id):
    if request.method == 'GET':
        plant = client.plants.plants.find_one({"id":_id})
        if plant is None:
            abort(404)
        plant.pop("_id")
        plant_type = client.plants.plant_types.find_one({"_id":plant["type"]})
        plant["type"] = plant_type["common_name"]
        plant = to_ascii(plant)
        return render_template("edit_plant.html", plant=plant)
    else:
        old_plant = client.plants.plants.find_one({"id":_id})
        if old_plant is None:
            abort(404)
        new_plant = parse_form(request.form)
        new_plant["_id"] = old_plant["_id"]
        _type = client.plants.plant_types.find_one({"common_name":new_plant["type"]})
        if _type is None:
            abort(500)
        new_plant["type"] = _type["_id"]
        client.plants.plants.save(new_plant)
        return redirect("/plants")

@flask_app.route("/plants/by-id/<_id>/delete.html")
def delete_plant(_id):
    client.plants.plants.remove({"id":_id})
    return redirect("/plants")

@flask_app.route("/plant_types.json")
def show_plant_types():
    types = []
    for _type in client.plants.plant_types.find(sort=[("common_name",1)]):
        _type.pop("_id")
        types.append(_type)
    return json.dumps(types)

@flask_app.route("/plants/types/new.html", methods=['GET','POST'])
def new_plant_type():
    if request.method == 'GET':
        return render_template("new_plant_type.html")
    else:
        _type = parse_form(request.form)
        old_type = client.plants.plant_types.find_one({"common_name":_type["common_name"]})
        if old_type is not None:
            abort(500)
        client.plants.plant_types.insert(_type)
        return redirect("/plants")

@flask_app.route("/plants/types/<common_name>")
def show_plant_type(common_name):
    plant_type = client.plants.plant_types.find_one({"common_name":common_name})
    if plant_type is None:
        abort(404)
    plant_type.pop("_id")
    return render_template("view_plant_type.html", plant_type=plant_type)

@flask_app.route("/plants/types/<common_name>/edit.html", methods=['GET','POST'])
def edit_plant_type(common_name):
    if request.method == 'GET':
        plant_type = client.plants.plant_types.find_one({"common_name":common_name})
        if plant_type is None:
            abort(404)
        plant_type.pop("_id")
        plant_type = to_ascii(plant_type)
        return render_template("edit_plant_type.html", plant_type=plant_type)
    else:
        old_type = client.plants.plant_types.find_one({"common_name":common_name})
        if old_type is None:
            abort(404)
        new_type = parse_form(request.form)
        new_type["_id"] = old_type["_id"]
        client.plants.plant_types.save(new_type)
        return redirect("/plants")

@flask_app.route("/plants/types/<common_name>/delete.html", methods=['GET'])
def delete_plant_type(common_name):
    client.plants.plant_types.remove({"common_name": common_name})
    return redirect("/plants")

# Plant types helper functions
def to_ascii(thing):
    # Converts a unicode thing returned by mongo to ascii
    if isinstance(thing, dict):
        res = {}
        for key, val in thing.iteritems():
            res[str(key)] = str(val) if type(val) in [unicode,str] else to_ascii(val)
        return res
    elif isinstance(thing, list):
        res = []
        for val in thing:
            res.append(str(val) if type(val) in [unicode,str] else to_ascii(val))
        return res
    else:
        return str(thing)
def parse_form(form):
    res = {}
    for key, val in form.iteritems():
        if "." in key:
            keys = key.split(".")
            _update(res,_to_dict(keys,val))
        else:
            res[key] = val
    for key, val in res.iteritems():
        if key[-1] == "]" and key[-3] == "[":
            new_key = key[:-3]
            new_i = int(key[-2])
            new_val = res.get(new_key,[])
            while len(new_val) <= new_i:
                new_val.append({})
            new_val[new_i] = val
            res[new_key] = new_val
            res.pop(key)
    print res
    return res
def _to_dict(keys,val):
    if len(keys) == 1:
        return {keys[0]: val}
    else:
        return {keys[0]: _to_dict(keys[1:],val)}
def _update(base, update):
    for key, val in update.iteritems():
        if isinstance(val, dict):
            base[key] = _update(base.get(key,{}), val)
            return base
        else:
            base[key] = val
            return base

@flask_app.template_filter("render_range")
def render_range(_range):
    if _range["min"] == _range["max"]:
        return _range["min"]
    else:
        return _range["min"] + " - " + _range["max"]

# Temporary
@flask_app.route("/plant_info")
def lookup_plant_info():
    KEY = "rfid"
    if not KEY in request.args:
        return "Error: no rfid code supplied"
    rfid = int(request.args[KEY])
    res = client.plants.plant_info.find_one({KEY: rfid})
    if res is None:
        i = 1
        while True:
            plant = client.plants.plant_info.find_one({"number": i})
            if not plant:
                client.plants.plant_info.insert({"rfid": rfid, "number": i})
                res = client.plants.plant_info.find_one({KEY: rfid})
                break
            else:
                i += 1
    res.pop("_id")
    return json.dumps(res)

@flask_app.route("/<database>")
def select_collection(database):
    if not database in DATABASE_NAMES:
        abort(404)
    colls = COLLECTION_NAMES[database]
    colls = OrderedDict([("/"+database+"/"+link, name)
        for link, name in colls.iteritems()])
    return render_template("collection_selection.html", collections=colls)

@flask_app.route("/<database>/<collection>")
def show_dashboard(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    title = COLLECTION_NAMES[database][collection]
    raw_initial_data = values.find_one(sort=[("date",-1)])
    if (now() - raw_initial_data["date"]) > 60:
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

@flask_app.route("/<database>/<collection>/hour_graphs.html")
def show_hour_graphs(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    info = COLLECTION_INFO[database][collection]
    return render_template("hour_graphs.html", info=info, database=database,
                            collection=collection)

@flask_app.route("/<database>/<collection>/hour_data.json")
def show_hour_data(database, collection):
    after_this_request(add_cache_header)
    values = values_collection(database, collection)
    if not values:
        abort(404)
    sensors = COLLECTION_INFO[database][collection]
    return json.dumps(raw_graphing_data(values,sensors,now()-60*60,now()))

@flask_app.route("/<database>/<collection>/day_graphs.html")
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

@flask_app.route("/<database>/<collection>/day_data.json")
def show_day_data(database, collection):
    values = values_collection(database, collection)
    if not values:
        abort(404)
    sensors = COLLECTION_INFO[database][collection]
    KEY = "date"
    if not KEY in request.args:
        abort(404)
    date_string = request.args[KEY]
    date = time.strptime(date_string, "%m/%d/%Y")
    date = time.mktime(date)
    if now() < date + 60*60*24: # The day has not ended, generate the data
        after_this_request(add_cache_header)
        return json.dumps(day_graphing_data(values, sensors, date))
    else: # The day has ended, serve a cached file
        cache_file = day_data_cache_file(database, collection, values, sensors,
                                        date_string)
        return flask_app.send_static_file(cache_file)

@flask_app.route("/<database>/<collection>/date_range_graphs.html")
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

@flask_app.route("/<database>/<collection>/date_range_data.json")
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
            curr_file_name = "./static/{}".format(curr_cache_file)
            curr_data = json.load(open(curr_file_name,'r'))
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

# Validates the database and collection values received and returns the relevant
# mongo collection of sensor values. If the input is invalid (the database or
# collection doesn't exist, this returns None
def values_collection(database, collection):
    if not database in DATABASE_NAMES:
        return None
    if not collection in COLLECTION_NAMES[database]:
        return None
    return client[database][collection]

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
        nulls = {sensor: None for sensor in sensors}
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
    date_string = time.strftime("%m/%d/%Y",date)
    date = time.mktime(date)
    date_string = date_string.replace("/","_")
    cache_file = "day_cache/{}/{}/{}.json".format(db,coll,date_string)
    cache_file_path = "./static/{}".format(cache_file)
    if not isfile(cache_file_path): # No cached file exists
        print "Generating cache file for {}".format(date_string)
        data = day_graphing_data(values, sensors, date)
        with open(cache_file_path, 'w+') as f:
            json.dump(data, f)
    return cache_file

# Edits the server response to tell the client not to cache this page
def add_cache_header(response):
    response.headers['Cache-Control'] = 'public,max-age=0,no-cache'
    return response

# Background thread that emits new data points to clients from the specified
# collection
def background_thread(system,board):
    values = client[system][board]
    count = values.count()
    namespace = "/{}/{}/data".format(system,board)
    sensors = COLLECTION_INFO[system][board]
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
        time.sleep(1)

# Helper function to get current timestamp
now = lambda: (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()

if __name__ == "__main__":
    for system in DATABASE_NAMES.keys():
        for collection in COLLECTION_NAMES[system].keys():
            # Start a thread to monitor the collection
            thread = Thread(target=background_thread, args=(system,collection))
            thread.daemon = True
            thread.start()
            # Make a socketio callback for the data namespace
            namespace = "/{}/{}/data".format(system,collection)
            socketio.on('connect',namespace=namespace)(lambda: None)
    socketio.run(flask_app, host='0.0.0.0')
