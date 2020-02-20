from google.appengine.ext import ndb

class EV(ndb.Model):
    # attributes of an ev
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    battery_size = ndb.FloatProperty()
    WLTP_range = ndb.FloatProperty()
    cost = ndb.FloatProperty()
    power = ndb.FloatProperty()
