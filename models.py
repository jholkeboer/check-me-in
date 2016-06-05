from google.appengine.ext import db
import json


class CheckIn(db.Model):
    owner = db.StringProperty(required=True)
    description = db.TextProperty()
    latitude = db.FloatProperty(required=True)
    longitude = db.FloatProperty(required=True)
    timestamp = db.IntegerProperty(required=True)