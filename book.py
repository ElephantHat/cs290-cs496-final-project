import webapp2
from google.appengine.ext import ndb
from cgi import escape
import json
import db_defs
import random

class Pub(webapp2.RequestHandler):
    def get(self, **kwargs):
        if 'id' not in kwargs:
            res = [{
            'key'       : x.key.integer_id(),
            'user'      : x.user,
            'username'   : db_defs.User.query(db_defs.User.token==x.user).fetch()[0].name,
            'title'     : x.title,
            'author'    : x.author,
            'coverurl'  : x.coverurl,
            'rating'    : x.rating,
            'comment'   : x.comment,
            'lat'       : x.lat,
            'lon'       : x.lon
        } for x in db_defs.Book.query(db_defs.Book.visible==True).order(-db_defs.Book.title).fetch()]
            self.response.write(json.dumps(res))
            return

        else:
            res= ndb.Key(db_defs.Book, int(kwargs['id'])).get().to_dict()
            if not res['visible']:
                self.response.write(json.dumps({'msg': "Could not find public book with id:" + kwargs['id']}))
            else:
                self.response.write(json.dumps(res))



class Book(webapp2.RequestHandler):
    def get(self, **kwargs):
        print kwargs


        token = self.request.get('token', default_value=None)
        if not token:
            self.response.write(json.dumps({'msg': 'Must be logged in to see book reviews.'}))
            return
        elif 'id' not in kwargs:
            res = [{
            'key'       : x.key.integer_id(),
            'user'      : x.user,
            'username'   : db_defs.User.query(db_defs.User.token==x.user).fetch()[0].name,
            'title'     : x.title,
            'author'    : x.author,
            'coverurl'  : x.coverurl,
            'rating'    : x.rating,
            'comment'   : x.comment,
            'lat'       : x.lat,
            'lon'       : x.lon
            } for x in db_defs.Book.query(db_defs.Book.user==int(token)).order(-db_defs.Book.title).fetch()]
            self.response.write(json.dumps(res))
            return

        else:
            res= ndb.Key(db_defs.Book, int(kwargs['id'])).get().to_dict()
            if res['user'] != int(token):
                self.response.write(json.dumps({'msg': "You don't have permission to view this review!"}))
                return
            self.response.write(json.dumps(res))

    def put(self, **kwargs):

        token = self.request.get('token', default_value=None)
        if not token:
            self.response.write(json.dumps({'msg': 'Must be logged in to edit book reviews.'}))
            return
        elif "id" not in kwargs:
            self.response.write(json.dumps({'msg': 'Cannot change entry without valid key.'}))
            return
        else:
            bkey = ndb.Key(db_defs.Book, int(kwargs['id']))
            newBook = bkey.get()

            if newBook.user != int(token):
                self.response.write(json.dumps({'msg': "You don't have permission to change this entry!"}))
                return

            #get values passed in http request
            title = self.request.get('title', default_value=None)
            author = self.request.get('author', default_value=None)
            visible = self.request.get('visible', default_value=False)
            rating = self.request.get('rating', default_value=None)
            comment = self.request.get('comment', default_value="No comment.")
            coverurl = self.request.get('coverurl', default_value="img/nothumb.png")
            lat = self.request.get('lat', default_value=None)
            lon = self.request.get('lon', default_value=None)


            if not title:
                self.response.write(json.dumps({'msg': 'Book title is required.'}))
                return
            else:
                newBook.title = escape(title)

            if not author:
                self.response.write(json.dumps({'msg': 'Book author is required.'}))
                return
            else:
                newBook.author = escape(author)

            if not rating:
                self.response.write(json.dumps({'msg': 'Book rating is required..'}))
                return
            else:
                newBook.rating = int(rating)

            if int(visible)==1:
                newBook.visible = True
            else:
                newBook.visible = False

            if lat:
                newBook.lat = float(lat)
            if lon:
                newBook.lon = float(lon)

            newBook.coverurl = coverurl

            newBook.comment = escape(comment)

            print newBook.to_dict()

            tempkey = newBook.put()
            print tempkey

            self.response.write(json.dumps({'msg': "Book review updated successfully!"}))
            return

    def delete(self, **kwargs):


        if 'tid' not in kwargs:
            self.response.write(json.dumps({'msg': 'Must be logged in to edit book reviews.'}))
            return

        elif "id" not in kwargs:
            self.response.write(json.dumps({'msg': 'Cannot delete entry without valid key.'}))
            return

        else:
            bkey = ndb.Key(db_defs.Book, int(kwargs['id']))
            newBook = bkey.get()

            if newBook.user != int(kwargs['tid']):
                self.response.write(json.dumps({'msg': "You don't have permission to change this entry!"}))
                return

            newBook.key.delete();
            self.response.write(json.dumps({'msg': 'Deletion Successful!', 'success': 'true'}))
            return

    def post(self):

        #make a new user in the database
        newBook = db_defs.Book()

        #get values passed in http request
        user = self.request.get('token', default_value=None)
        title = self.request.get('title', default_value=None)
        author = self.request.get('author', default_value=None)
        visible = self.request.get('visible', default_value=False)
        rating = self.request.get('rating', default_value=None)
        comment = self.request.get('comment', default_value="No comment.")
        coverurl = self.request.get('coverurl', default_value="img/nothumb.png")
        lat = self.request.get('lat', default_value=None)
        lon = self.request.get('lon', default_value=None)



        if not user:
            self.response.write(json.dumps({'msg': 'Must be logged in to add books.'}))
            return
        else:
            newBook.user = int(user)

        if not title:
            self.response.write(json.dumps({'msg': 'Book title is required.'}))
            return
        else:
            newBook.title = escape(title)

        if not author:
            self.response.write(json.dumps({'msg': 'Book author is required.'}))
            return
        else:
            newBook.author = escape(author)

        if not rating:
            self.response.write(json.dumps({'msg': 'Book rating is required..'}))
            return
        elif int(rating) < 0 or int(rating) > 5 or rating == "":
            self.response.write(json.dumps({'msg': 'Book rating must be in range 0-5.'}))
            return
        else:
            newBook.rating = int(rating)

        if not coverurl:
            newBook.coverurl = "img/nothumb.png"
        else:
            newBook.coverurl = coverurl

        if int(visible)==1:
            newBook.visible = True
        else:
            newBook.visible = False

        if comment == "":
            newBook.comment = "No comment."
        else:
            newBook.comment = escape(comment)

        if lat:
            newBook.lat = float(lat)
        if lon:
            newBook.lon = float(lon)



        newBook.put()

        self.response.write(json.dumps({'msg': "Book review added successfully!"}))
        return
