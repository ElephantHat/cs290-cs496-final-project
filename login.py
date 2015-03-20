import webapp2
from google.appengine.ext import ndb
from cgi import escape
import json
import db_defs
import random

class Login(webapp2.RequestHandler):
    def get(self):
        self.response.status = 503
        self.response.status_message = "Forbidden. Login requests must be made via POST."
        output = {"response": 503, "msg": "Forbidden. Login requests must be made via POST."}
        self.response.write(json.dumps(output))
        return

    def put(self):
        self.response.status = 503
        self.response.status_message = "Forbidden. Login requests must be made via POST."
        return

    def delete(self):
        self.response.status = 503
        self.response.status_message = "Forbidden. Login requests must be made via POST."
        return

    def post(self):
        #get values passed in http request
        username = self.request.get('uname', default_value=None)
        password = self.request.get('pw', default_value=None)
        name = self.request.get('name', default_value="Anonymous")
        if name == "":
            name = "Anonymous"

        #make a new user in the database
        newUser = db_defs.User()

        #if username & password were supplied, and the username isn't already in use, add user to database. If user exists, compare passwords and log in if they match
        if username:
            uq = [x.uname for x in db_defs.User.query(db_defs.User.uname==username).fetch()]
            tq = [x.token for x in db_defs.User.query().fetch()]

            if username not in uq:
                if password:
                    newUser.uname = username
                    newUser.pw = password
                    newUser.name = escape(name)

                    #generate unique access token
                    while True:
                        token = random.randint(100000, 999999)
                        if token not in tq:
                            newUser.token = token
                            break

                    newUser.put()

                    self.response.write(json.dumps({'msg': 'User added!', 'token': token, 'username':name}))
                    return

                else:
                    self.response.status = 401
                    self.response.write(json.dumps({'msg': 'Password is required.'}))
                    return
            elif password:
                u = db_defs.User.query(db_defs.User.uname==username).fetch()
                if password==u[0].pw:
                    self.response.write(json.dumps({'msg': 'Logged in!', 'token': u[0].token, 'username': u[0].name}))
                    return
                else:
                    self.response.status = 401
                    self.response.write('That username exists. If you are trying to log in, you have an incorrect password.')
                    return
            else:
                self.response.status = 401
                return

        else:
            self.response.status = 401
            self.response.write(json.dumps({'msg': 'Username is required.'}))
            return
