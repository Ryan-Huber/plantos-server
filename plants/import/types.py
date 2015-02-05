#!/usr/bin/env python

from mongoengine import connect
from mongoengine import Document, EmbeddedDocument
from mongoengine import fields
connect("cityfarm")

class Range(EmbeddedDocument):
    minimum = fields.IntField()
    maximum = fields.IntField()
class PlantType(Document):
    common_name = fields.StringField(required=True)
    latin_name = fields.StringField(required=True)
    cultivar = fields.StringField()
    conv_dtg = fields.EmbeddedDocumentField(Range)
    conv_dtm = fields.EmbeddedDocumentField(Range)
    native_to = fields.StringField()

import csv
with open("types.csv") as typesfile:
    reader = csv.DictReader(typesfile)
    for row in reader:
        for key in ["conv_dtg", "conv_dtm"]:
            range = row[key]
            if range is '':
                row[key] = Range()
            elif not "-" in range:
                row[key] = Range(minimum=int(range), maximum=int(range))
            else:
                print range
