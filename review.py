from google.appengine.ext import ndb

class Review(ndb.Model):

    comment = ndb.StringProperty(required=True)
    rating = ndb.IntegerProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now=True)
