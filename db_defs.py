from google.appengine.ext import ndb
import datetime

class Character(ndb.Model):
    name = ndb.StringProperty(required=True)
    race = ndb.StringProperty(required=True)
    cclass = ndb.StringProperty(required=True)
    age = ndb.IntegerProperty(required=True)
    npc = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now=True, required=True)

class User(ndb.Model):
    uname = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    pw = ndb.StringProperty(required=True)
    token = ndb.IntegerProperty(required=True)

class Book(ndb.Model):
    def to_dict(self): #shamelessly stolen from lecture vid for debugging
        d = super(Book, self).to_dict()
        d['key'] = self.key.id()
        return d

    user = ndb.IntegerProperty(required=True)
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    visible = ndb.BooleanProperty(required=True)
    coverurl = ndb.StringProperty(required=True)
    rating = ndb.IntegerProperty(required=True)
    comment = ndb.StringProperty(required=True)
    lat = ndb.FloatProperty(required=False)
    lon = ndb.FloatProperty(required=False)
