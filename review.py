from google.appengine.ext import ndb

# Review class
class Review(ndb.Model):
    # A model for representing an individual review
    comment = ndb.StringProperty(required=True)
    rating = ndb.IntegerProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now=True)
