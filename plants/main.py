#!/usr/bin/env python

# Database info from sensors/constants.py
from sensors.constants import DATABASE_NAMES
from sensors.constants import COLLECTION_NAMES
from sensors.constants import COLLECTION_INFO

# Flask setup
from flask import abort
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
bp = Blueprint('plants', __name__, static_folder="static",
        template_folder="templates", url_prefix="/plants")
# Mongoengine imports
from mongoengine import CASCADE
from mongoengine import fields as mefields
from mongoengine import Document, EmbeddedDocument
from bson.objectid import ObjectId
# JSON Setup
from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return JSONEncoder.default(self, o)
json = MyEncoder()
# WTForms setup
from wtforms import Form
from wtforms import fields as wtfields
from wtforms import validators
from datetime import datetime
from wtforms.ext.dateutil import fields as datewtfields
class MultiDict(dict):
    def getlist(self, key):
        value = self[key]
        if not isinstance(value, list):
            value = [value]
        return value


###################
# Database models #
###################

class Range(EmbeddedDocument):
    minimum = mefields.IntField()
    maximum = mefields.IntField()
    def to_string(self):
        if self.maximum is None and self.minimum is None:
            return ""
        elif (self.maximum is None) ^ (self.minimum is None):
            return str(self.maximum or self.minimum)
        elif self.maximum == self.minimum:
            return str(self.minimum)
        else:
            return "%d - %d" % (self.minimum, self.maximum)

class PlantType(Document):
    common_name = mefields.StringField(required=True)
    latin_name = mefields.StringField(required=True)
    cultivar = mefields.StringField()
    conv_dtg = mefields.EmbeddedDocumentField(Range)
    conv_dtm = mefields.EmbeddedDocumentField(Range)
    native_to = mefields.StringField()

class Note(EmbeddedDocument):
    date = mefields.DateTimeField(required=True)
    content = mefields.StringField(required=True)

class Plant(Document):
    type = mefields.ReferenceField(PlantType, required=True,
            reverse_delete_rule=CASCADE)
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

class RangeForm(Form):
    minimum = wtfields.IntegerField("Minimum", [validators.optional()])
    maximum = wtfields.IntegerField("Maximum", [validators.optional()])
    def validate_minimum(form, field):
        error = "If a minimum is provided then a maximum must also be provided"
        if form.maximum.data is None:
            raise validators.ValidationError(error)
    def validate_maximum(form, field):
        error = "If a maximum is provided then a minimum must also be provided"
        if form.minimum.data is None:
            raise validators.ValidationError(error)
        error = "The maximum must be greater than or equal to the minimum"
        if form.minimum.data > form.maximum.data:
            raise validators.ValidationError(error)

class PlantTypeForm(Form):
    common_name = wtfields.StringField("Common Name", [validators.required()])
    latin_name = wtfields.StringField("Latin Name", [validators.required()])
    cultivar = wtfields.StringField("Cultivar", [validators.optional()])
    conv_dtg = wtfields.FormField(RangeForm, "Conventional Days to Germination")
    conv_dtm = wtfields.FormField(RangeForm, "Conventional Days to Maturity")
    native_to = wtfields.StringField("Native To", [validators.optional()])
    def create_type(self):
        new_type = PlantType(**{k:v.data for k,v in self._fields.iteritems()})
        new_type.save()
        return new_type
    def update_type(self, plant_type):
        for k,v in self._fields.iteritems():
            self.update_object_field(plant_type, k, v.data)
        plant_type.save()
        return plant_type
    def update_object_field(self, obj, key, value):
        if isinstance(value, dict):
            for subkey, subvalue in value.iteritems():
                self.update_object_field(obj[key], subkey, subvalue)
        else:
            obj[key] = value
        return obj

class Note(Form):
    date = wtfields.DateTimeField("Date", [validators.required()])
    content = wtfields.StringField("Content", [validators.required()])

class PlantForm(Form):
    type = wtfields.SelectField("Type", [validators.required()], coerce=ObjectId)
    number = wtfields.IntegerField("Number", [validators.required()])
    date_planted = datewtfields.DateTimeField("Date Planted",
            [validators.optional()])
    radicle_emergence = datewtfields.DateTimeField("Radicle Emergence",
            [validators.optional()])
    hypocotyl_emergence = datewtfields.DateTimeField("Hypocotyl Emergence",
            [validators.optional()])
    foliage_emergence = datewtfields.DateTimeField("Foliage Emergence",
            [validators.optional()])
    date_of_transfer = datewtfields.DateTimeField("Date of Transfer",
            [validators.optional()])
    date_of_harvest = datewtfields.DateTimeField("Date of Harvest",
            [validators.optional()])
    def __init__(self, values):
        for key,value in values.iteritems():
            if isinstance(value, datetime):
                values[key] = str(value)
        super(PlantForm, self).__init__(values)
        self.type.choices = [(type.id, type.common_name) for type in
                PlantType.objects]
    def create_plant(self):
        new_plant = Plant(**{k:v.data for k,v in self._fields.iteritems()})
        new_plant.save()
        return new_plant
    def update_plant(self, plant):
        for k,v in self._fields.iteritems():
            if k == "type":
                pt = PlantType.objects(id=v.data).first()
                plant[k] = pt
            else:
                plant[k] = v.data
        plant.save()
        return plant


@bp.route("/")
def index():
    databases = DATABASE_NAMES
    return render_template("plants/plants.html", databases=DATABASE_NAMES)

@bp.route("/plants.json")
def list_plants():
    params = {}
    if "type_id" in request.args:
        type_id = request.args["type_id"]
        plant_type = PlantType.objects(id=type_id)
        if not plant_type:
            abort(404)
        params["type"] = plant_type[0].id
    plants = Plant.objects(**params)
    plants_info = []
    for plant in plants:
        plant_info = plant.to_mongo()
        plant_info["type"] = plant.type.to_mongo()
        plants_info.append(plant_info)
    return json.encode(plants_info)

@bp.route("/plants/<id>")
def view_plant(id):
    plant = Plant.objects(id=id).first()
    if plant is None:
        abort(404)
    return render_template("plants/view_plant.html", plant=plant)

@bp.route("/plants/new.html", methods=['GET','POST'])
def new_plant():
    form = PlantForm(request.form)
    if request.method == 'POST' and form.validate():
        plant = form.create_plant()
        return redirect(url_for("plants.view_plant", id=plant.id))
    return render_template("plants/edit_plant.html", form=form)

@bp.route("/plants/<id>/edit.html", methods=['GET','POST'])
def edit_plant(id):
    plant = Plant.objects(id=id).first()
    if plant is None:
        abort(404)
    if request.method == 'GET':
        form = PlantForm(MultiDict(plant.to_mongo()))
    else:
        form = PlantForm(request.form)
        if form.validate():
            plant = form.update_plant(plant)
            return redirect(url_for("plants.view_plant", id=plant.id))
    return render_template("plants/edit_plant.html", form=form,
            plant_id=plant.id)

@bp.route("/plants/<id>/delete.html", methods=['POST'])
def delete_plant(id):
    plant = Plant.objects(id=id).first()
    if plant is None:
        abort(404)
    plant.delete()
    return redirect(url_for("plants.index"))

@bp.route("/plant_types.json")
def list_plant_types():
    plant_types = [pt.to_mongo() for pt in PlantType.objects.all()]
    return json.encode(plant_types)

@bp.route("/types/<id>")
def view_plant_type(id):
    plant_type = PlantType.objects(id=id).first()
    if plant_type is None:
        abort(404)
    return render_template("plants/view_plant_type.html", plant_type=plant_type)

@bp.route("/types/new.html", methods=['GET','POST'])
def new_plant_type():
    form = PlantTypeForm(request.form)
    if request.method == 'POST' and form.validate():
        plant_type = form.create_type()
        return redirect(url_for("plants.view_plant_type", id=plant_type.id))
    return render_template("/plants/edit_plant_type.html", form=form)

@bp.route("/types/<id>/edit.html", methods=['GET','POST'])
def edit_plant_type(id):
    plant_type = PlantType.objects(id=id).first()
    if plant_type is None:
        abort(404)
    if request.method == 'GET':
        form = PlantTypeForm(MultiDict(flatten(plant_type.to_mongo())))
    else:
        form = PlantTypeForm(request.form)
        if form.validate():
            form.update_type(plant_type)
            return redirect(url_for("plants.view_plant_type", id=plant_type.id))
    return render_template("plants/edit_plant_type.html", form=form,
            plant_type_id=plant_type.id)

@bp.route("/types/<id>/delete.html", methods=['POST'])
def delete_plant_type(id):
    plant_type = PlantType.objects(id=id).first()
    if plant_type is None:
        abort(404)
    plant_type.delete()
    return redirect(url_for("plants.index"))

# Flattens a dictionary returned by calling to_mongo on a Document so that a
# Form can correctly read nested data
def flatten(d):
    for k,v in d.iteritems():
        if isinstance(v, dict):
            v = flatten(v)
            for subk, subv in v.iteritems():
                d["%s-%s" % (k, subk)] = subv
            d.pop(k)
    return d

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__, template_folder="../templates",
            static_folder="../static", instance_relative_config=True)
    app.config.from_pyfile("application.cfg")
    @app.route("/", endpoint="index")
    def real_index():
        return render_template("index.html")
    from flask.ext.mongoengine import MongoEngine
    app.mongoengine = MongoEngine(app)
    app.register_blueprint(bp)
    app.run(debug=True)
