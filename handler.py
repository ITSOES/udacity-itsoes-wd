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
import os
import hmac
import random
from string import letters

import webapp2
import jinja2
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
folders = ['', 'Unit2', 'Unit3', 'Unit4']
paths = [os.path.join(template_dir, x) for x in folders]
loader = jinja2.FileSystemLoader(paths)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
del paths, loader, folders, template_dir  # Deletes the helper variables after use

SECRET = 'whatev'

def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

def hasher(s, salt='', saltit=None):
    if not (salt and saltit) or saltit == False:
        return hmac.new(SECRET, str(s)).hexdigest()
    salt = salt or make_salt()
    return hasher(s + salt)

def make_secure(s, salt='', saltit=None):
    # if not (salt and saltit) or saltit == False:
    #     return hmac.new(SECRET, str(s)).hexdigest()
    # salt = salt or make_salt()
    return '%s|%s' % (str(s), hasher(s))

def check_secure_val(sHASH):
    s = sHASH.split('|')[0] if sHASH else ''
    return sHASH == make_secure(s) and s

class Handler(webapp2.RequestHandler):
    def initialize(self, *a, **kw):
        # print(Sitemodel.by_id(4))
        # print(testClass.by_id(4))
        super(Handler, self).initialize(*a, **kw)
        uid = self.readcookie('user_id')
        self.user = uid and Sitemodel.by_id(uid)

    def renderjinja(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def setcookie(self, name, data):
        # print('NAME', name, 'DATA', data, 'SECURE', make_secure(data))
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, make_secure(data)))

    def readcookie(self, name, default='', numbered=False):
        result = check_secure_val(self.request.cookies.get(str(name))) or default
        if numbered:
            try: return int(result)
            except: return 0
        return result

    def hash_password(self, string):
        return hasher(string)



class Homepage(Handler):
    def get(self):
        self.renderjinja('Homepage.html')

class GoHome(Handler):
    def get(self):
        self.redirect("/")

class Sitemodel(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    lastmodified = db.DateTimeProperty(auto_now=True)

    def addEmail(self):
        pass

    @classmethod
    def by_id(cls, uid):
        user = cls.get_by_id(uid)
        return user

    @classmethod
    def by_key(cls, **key):
        pass
        print('KEY', key)
        for key, value in key.items():
            u = cls.all().filter(key+' =', value).get()
            return u


    @classmethod
    def register(cls, name, password, email=None):
        p = make_secure(password)
        return cls(name=name, password_hash=p, email=email)


app = webapp2.WSGIApplication([ ('/', Homepage),
                                ('.*', GoHome)  # Redirects any junk url home
                              ], debug=True)
