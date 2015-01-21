#!/usr/bin/env python

# General imports
import HTMLParser
# Flask setup
from flask import abort
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
plants = Blueprint('plants', __name__, static_folder="static",
                    template_folder="templates", url_prefix="/plants")
# Mongoengine imports
from mongoengine import fields as mefields
from mongoengine import Document, EmbeddedDocument
# JSON Setup
from json import JSONEncoder
from bson.objectid import ObjectId
class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(o)
json = MyEncoder()
# WTForms setup
from wtforms import Form
from wtforms import fields as wtfields
from wtforms import validators
class MultiDict(object):
    def getlist(self, key):
        value = self[key]
        if not isinstance(value, list):
            value = [value]
        return value


###################
# Database models #
###################

class PlantType(Document, MultiDict):
    common_name = mefields.StringField(required=True)
    latin_name = mefields.StringField(required=True)
    min_conv_dtg = mefields.IntField(required=True)
    max_conv_dtg = mefields.IntField(required=True)
    min_conv_dtm = mefields.IntField(required=True)
    max_conv_dtm = mefields.IntField(required=True)
    cultivar = mefields.StringField(required=True)
    native_to = mefields.StringField(required=True)

class Note(EmbeddedDocument):
    date = mefields.DateTimeField(required=True)
    content = mefields.DateTimeField(required=True)

class Plant(Document):
    type = mefields.ReferenceField(PlantType, required=True)
    number = mefields.IntField(required=True)
    date_planted = mefields.DateTimeField()
    radicle_emergence = mefields.DateTimeField()
    hypocotyl_emergence = mefields.DateTimeField()
    foliage_emergence = mefields.DateTimeField()
    date_of_transfer = mefields.DateTimeField()
    date_of_harvest = mefields.DateTimeField()
    notes = mefields.ListField(mefields.EmbeddedDocumentField(Note))

#########
# Forms #
#########

class PlantTypeForm(Form):
    common_name = wtfields.StringField("Common Name", [validators.required()])
    latin_name = wtfields.StringField("Latin Name", [validators.required()])
    min_conv_dtg = wtfields.IntegerField("Minimum Days to Germination",
            [validators.required()])
    max_conv_dtg = wtfields.IntegerField("Maximum Days to Germination",
            [validators.required()])
    min_conv_dtm = wtfields.IntegerField("Minimum Days to Maturity",
            [validators.required()])
    max_conv_dtm = wtfields.IntegerField("Maximum Days to Maturity",
            [validators.required()])
    cultivar = wtfields.StringField("Cultivar", [validators.required()])
    native_to = wtfields.StringField("Native To", [validators.required()])
    def create_type(self):
        new_type = PlantType(**{k:v.data for k,v in self._fields.iteritems()})
        new_type.save()
        return new_type
    def update_type(self, plant_type):
        for k,v in self._fields.iteritems():
            plant_type[k] = v.data
            plant_type.save()


# Root page
@plants.route("/")
def browse_plants():
    return render_template("plants.html")

# This page dumps a JSON array of all of the plants in the database
# Arguments:
#   type_id (optional): filters the results to only show plants of the type with
#     the given id
@plants.route("/plants.json")
def show_plants():
    params = {}
    if "type_id" in request.args:
        type_id = unescape_html(request.args["type_id"])
        params["plant_type"] = PlantType.objects.get_or_404(id=type_id)
    plants = [plant.to_mongo() for plant in Plant.objects(**params)]
    return json.encode(plants)

# This page displays information about a plant with the given id
@plants.route("/plants/<_id>")
def show_plant(_id):
    plant = PlantType.objects.get_or_404(id=_id)
    return render_template("view_plant.html", plant=json.encode(plant))

# This page displays a form to create a new plant entry in the database
@plants.route("/plants/new.html", methods=['GET','POST'])
def new_plant():
    if request.method == 'GET':
        return render_template("edit_plant.html", plant=None)
    else:
        plant = parse_form(request.form)
        if not "events" in plant:
            plant["events"] = []
        if not _reference_type(plant):
            abort(500)
        old_plant = db().plants.find_one({"id": plant["id"]})
        if old_plant is not None:
            abort(500)
        db().plants.insert(plant)
        return redirect("/plants")

# This page displays a form to edit an existing plant entry in the database
@plants.route("/plants/<_id>/edit.html", methods=['GET','POST'])
def edit_plant(_id):
    if request.method == 'GET':
        plant = db().plants.find_one({"id":_id})
        if plant is None:
            abort(404)
        if not _dereference_type(plant):
            abort(500)
        return render_template("edit_plant.html", plant=to_ascii(plant))
    else:
        old_plant = db().plants.find_one({"id":_id})
        if old_plant is None:
            abort(404)
        new_plant = parse_form(request.form)
        if not _reference_type(new_plant):
            abort(500)
        new_plant["_id"] = old_plant["_id"]
        db().plants.save(new_plant)
        return redirect("/plants")

# This page displays a simple confirmation form which when submitted, deletes
# the relevant plant from the database
@plants.route("/plants/<_id>/delete.html", methods=['GET','POST'])
def delete_plant(_id):
    if request.method == 'GET':
        plant = db().plants.find_one({"id":_id})
        if plant is None:
            abort(404)
        if not _dereference_type(plant):
            abort(500)
        return render_template("delete_plant.html", plant=plant)
    else:
        db().plants.remove({"id":_id})
        return redirect("/plants")

@plants.route("/plant_types.json")
def show_plant_types():
    plant_types = [pt.to_mongo() for pt in PlantType.objects()]
    return json.encode(plant_types)

@plants.route("/types/<id>")
def show_plant_type(id):
    plant_type = PlantType.objects(id=id)[0]
    if plant_type is None:
        abort(404)
    return render_template("view_plant_type.html", plant_type=plant_type)

@plants.route("/types/new.html", methods=['GET','POST'])
def new_plant_type():
    form = PlantTypeForm(request.form)
    if request.method == 'POST' and form.validate():
        form.create_type()
        return redirect("/plants")
    return render_template("edit_plant_type.html", form=form, plant_type=None)

@plants.route("/types/<id>/edit.html", methods=['GET','POST'])
def edit_plant_type(id):
    plant_type = PlantType.objects(id=id)[0]
    if plant_type is None:
        abort(404)
    if request.method == 'GET':
        form = PlantTypeForm(plant_type)
        return render_template("edit_plant_type.html", form=form,
                plant_type=plant_type)
    else:
        form = PlantTypeForm(request.form)
        if form.validate():
            form.update_type(plant_type)
            return redirect("/plants")
        else:
            return render_template("edit_plant_type.html", form=form,
                    plant_type=plant_type)

@plants.route("/types/<id>/delete.html", methods=['POST'])
def delete_plant_type(id):
    plant_type = PlantType.objects(id=id)[0]
    if plant_type is None:
        abort(404)
    plant_type.delete()
    return redirect("/plants")


# Temporary
@plants.route("/plant_info")
def lookup_plant_info():
    KEY = "rfid"
    if not KEY in request.args:
        return "Error: no rfid code supplied"
    rfid = int(request.args[KEY])
    res = db().plant_info.find_one({KEY: rfid})
    if res is None:
        i = 1
        while True:
            plant = db().plant_info.find_one({"number": i})
            if not plant:
                db().plant_info.insert({"rfid": rfid, "number": i})
                res = db().plant_info.find_one({KEY: rfid})
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
    plant_type = db().plant_types.find_one({"_id":plant["type"]})
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
    plant_type = db().plant_types.find_one({"common_name":plant["type"]})
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
html_parser = None
def unescape_html(string):
    global html_parser
    if html_parser is None:
        html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(string)
