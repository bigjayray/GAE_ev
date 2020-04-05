from google.appengine.ext import ndb
from review import Review

# EV class
class EV(ndb.Model):
    # A model for representing an individual an ev
    name = ndb.StringProperty(required=True)
    manufacturer = ndb.StringProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    battery_size = ndb.FloatProperty(required=True)
    WLTP_range = ndb.FloatProperty(required=True)
    cost = ndb.FloatProperty(required=True)
    power = ndb.FloatProperty(required=True)
    reviews = ndb.StructuredProperty(Review, repeated=True)
    rating = ndb.FloatProperty()
