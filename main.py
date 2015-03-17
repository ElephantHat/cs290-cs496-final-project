#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import template_wrangler
from google.appengine.ext import ndb
import db_defs
from time import sleep
import datetime
import string

class MainHandler(template_wrangler.TemplateHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_variables = {}

    def render(self, page):
        template_wrangler.TemplateHandler.render(self, page, self.template_variables)

    def get(self):
        self.render('index.html')

    def post(self):
        self.render('index.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
app.router.add(webapp2.Route('/login', 'login.Login'))
app.router.add(webapp2.Route('/book', 'book.Book'))
app.router.add(webapp2.Route(r'/book/<id:[0-9]+><:/?>', 'book.Book'))
app.router.add(webapp2.Route(r'/book/<id:[0-9]+><:/><tid:[0-9]+>', 'book.Book'))
app.router.add(webapp2.Route(r'/public/<id:[0-9]+><:/?>', 'book.Pub'))
app.router.add(webapp2.Route('/public', 'book.Pub'))
