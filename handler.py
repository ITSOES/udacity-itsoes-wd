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
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
folders = ['', 'Unit2', 'Unit3', 'Unit4']
paths = [os.path.join(template_dir, x) for x in folders]
loader = jinja2.FileSystemLoader(paths)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
del paths, loader, folders, template_dir  # Deletes the helper variables after use


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def renderjinja(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def setcookie(self):
        pass

class Homepage(Handler):
    def get(self):
        self.renderjinja('Homepage.html')

class GoHome(Handler):
    def get(self):
        self.redirect("/")

app = webapp2.WSGIApplication([ ('/', Homepage),
                                ('.*', GoHome)
                              ], debug=True)