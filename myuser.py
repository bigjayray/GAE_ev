from google.appengine.ext import ndb

# MyUser class
class MyUser(ndb.Model):
    # A model for representing an individual user
    email_address = ndb.StringProperty()
