#!/usr/bin/env python

# General imports
import json
import HTMLParser
# Flask setup
from flask import abort
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
plants = Blueprint('plants', __name__, static_folder="static",
                    template_folder="templates", url_prefix="/plants")
# PyMongo setup
from pymongo import MongoClient
client = MongoClient()
with open("/var/lib/plantos-server/database_credentials.txt","r") as f:
    (username,password) = f.readline()[:-1].split(",")
client.admin.authenticate(username,password)
db = client.plants

# Root page
@plants.route("/")
def browse_plants():
    return render_template("plants.html")

# This page dumps a JSON array of all of the plants in the database
# Arguments:
#   type (optional): filters the results to only show plants of the given type
@plants.route("/plants.json")
def show_plants():
    plants = []
    for plant in db.plants.find(sort=[("id",1)]):
        plant.pop("_id")
        if not _dereference_type(plant):
            abort(500)
        plants.append(plant)
    if "type" in request.args:
        _type = unescape_html(request.args["type"])
        plants = [p for p in plants if p["type"]["common_name"] == _type]
    return json.dumps(plants)

# This page displays information about a plant with the given id
@plants.route("/by-id/<_id>")
def show_plant(_id):
    plant = db.plants.find_one({"id":_id})
    if plant is None:
        abort(404)
    if not _dereference_type(plant):
        abort(500)
    plant.pop("_id")
    plant["type"]["conv_dtg"] = render_range(plant["type"]["conv_dtg"])
    plant["type"]["conv_dtm"] = render_range(plant["type"]["conv_dtm"])
    for i in range(len(plant["events"])):
        plant["events"][i]["location"]["site"] = \
            render_coordinates(plant["events"][i]["location"]["site"])
    return render_template("view_plant.html", plant=plant)

# This page displays a form to create a new plant entry in the database
@plants.route("/by-id/new.html", methods=['GET','POST'])
def new_plant():
    if request.method == 'GET':
        return render_template("edit_plant.html", plant=None)
    else:
        plant = parse_form(request.form)
        if not "events" in plant:
            plant["events"] = []
        if not _reference_type(plant):
            abort(500)
        old_plant = db.plants.find_one({"id": plant["id"]})
        if old_plant is not None:
            abort(500)
        db.plants.insert(plant)
        return redirect("/plants")

# This page displays a form to edit an existing plant entry in the database
@plants.route("/by-id/<_id>/edit.html", methods=['GET','POST'])
def edit_plant(_id):
    if request.method == 'GET':
        plant = db.plants.find_one({"id":_id})
        if plant is None:
            abort(404)
        if not _dereference_type(plant):
            abort(500)
        return render_template("edit_plant.html", plant=to_ascii(plant))
    else:
        old_plant = db.plants.find_one({"id":_id})
        if old_plant is None:
            abort(404)
        new_plant = parse_form(request.form)
        if not _reference_type(new_plant):
            abort(500)
        new_plant["_id"] = old_plant["_id"]
        db.plants.save(new_plant)
        return redirect("/plants")

# This page displays a simple confirmation form which when submitted, deletes
# the relevant plant from the database
@plants.route("/by-id/<_id>/delete.html", methods=['GET','POST'])
def delete_plant(_id):
    if request.method == 'GET':
        plant = db.plants.find_one({"id":_id})
        if plant is None:
            abort(404)
        if not _dereference_type(plant):
            abort(500)
        return render_template("delete_plant.html", plant=plant)
    else:
        db.plants.remove({"id":_id})
        return redirect("/plants")

@plants.route("/plant_types.json")
def show_plant_types():
    types = []
    for _type in db.plant_types.find(sort=[("common_name",1)]):
        _type.pop("_id")
        types.append(_type)
    return json.dumps(types)

@plants.route("/types/<common_name>")
def show_plant_type(common_name):
    plant_type = db.plant_types.find_one({"common_name":common_name})
    if plant_type is None:
        abort(404)
    plant_type.pop("_id")
    plant_type["conv_dtg"] = render_range(plant_type["conv_dtg"])
    plant_type["conv_dtm"] = render_range(plant_type["conv_dtm"])
    return render_template("view_plant_type.html", plant_type=plant_type)

@plants.route("/types/new.html", methods=['GET','POST'])
def new_plant_type():
    if request.method == 'GET':
        return render_template("edit_plant_type.html", plant_type=None)
    else:
        _type = parse_form(request.form)
        old_type = db.plant_types.find_one({"common_name":_type["common_name"]})
        if old_type is not None:
            abort(500)
        db.plant_types.insert(_type)
        return redirect("/plants")

@plants.route("/types/<common_name>/edit.html", methods=['GET','POST'])
def edit_plant_type(common_name):
    if request.method == 'GET':
        plant_type = db.plant_types.find_one({"common_name":common_name})
        if plant_type is None:
            abort(404)
        plant_type.pop("_id")
        plant_type = to_ascii(plant_type)
        return render_template("edit_plant_type.html", plant_type=plant_type)
    else:
        old_type = db.plant_types.find_one({"common_name":common_name})
        if old_type is None:
            abort(404)
        new_type = parse_form(request.form)
        new_type["_id"] = old_type["_id"]
        db.plant_types.save(new_type)
        return redirect("/plants")

@plants.route("/types/<common_name>/delete.html", methods=['GET','POST'])
def delete_plant_type(common_name):
    if request.method == 'GET':
        plant_type = db.plant_types.find_one({"common_name": common_name})
        if plant_type is None:
            abort(404)
        return render_template("delete_plant_type.html", plant_type=plant_type)
    else:
        plant_type = db.plant_types.find_one({"common_name": common_name})
        db.plants.remove({"type": plant_type["_id"]})
        db.plant_types.remove({"common_name": common_name})
        return redirect("/plants")


# Temporary
@plants.route("/plant_info")
def lookup_plant_info():
    KEY = "rfid"
    if not KEY in request.args:
        return "Error: no rfid code supplied"
    rfid = int(request.args[KEY])
    res = db.plant_info.find_one({KEY: rfid})
    if res is None:
        i = 1
        while True:
            plant = db.plant_info.find_one({"number": i})
            if not plant:
                db.plant_info.insert({"rfid": rfid, "number": i})
                res = db.plant_info.find_one({KEY: rfid})
                break
            else:
                i += 1
    res.pop("_id")
    return json.dumps(res)

########################
#                      #
#   Helper Functions   #
#                      #
########################
# Plants usually have a reference to a type stored in their "type" attribute.
# This function takes in a plant and replaces this reference with the info of
# the plant type itself
# Returns a boolean indicating success
def _dereference_type(plant):
    plant_type = db.plant_types.find_one({"_id":plant["type"]})
    if plant_type is None:
        return False
    else:
        plant_type.pop("_id")
        plant["type"] = plant_type
        return True
# This is the opposite of _dereference_type. It takes in a plant and replaces
# it's "type" attribute with the id of the plant type
# Returns a boolean indicating success
def _reference_type(plant):
    plant_type = db.plant_types.find_one({"common_name":plant["type"]})
    if plant_type is None:
        return False
    else:
        plant["type"] = plant_type["_id"]
        return True
# Converts a unicode thing returned by mongo to ascii
def to_ascii(thing):
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
# On a POST request from a form, we receive a flat dictionary of encoded keys
# and values. This takes that dictionary and turns it into a more useful non-
# flat dictionary
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
    return res
# Helper function for parse_form
def _to_dict(keys,val):
    if len(keys) == 1:
        return {keys[0]: val}
    else:
        return {keys[0]: _to_dict(keys[1:],val)}
# Helper function for parse_form
def _update(base, update):
    for key, val in update.iteritems():
        if isinstance(val, dict):
            base[key] = _update(base.get(key,{}), val)
            return base
        else:
            base[key] = val
            return base
# Used to render the days to germination/maturity values for plant types
def render_range(_range):
    if _range["min"] == _range["max"]:
        return _range["min"]
    else:
        return _range["min"] + " - " + _range["max"]
# Used to render the cup site for plants
def render_coordinates(coord):
    return "({}, {})".format(coord["x"],coord["y"])
# Parses out weird html encoded strings like &#39 for '
def unescape_html(string):
    parser = HTMLParser.HTMLParser()
    return parser.unescape(string)
