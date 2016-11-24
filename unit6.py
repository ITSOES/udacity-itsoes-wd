import webapp2, logging

from handler import Handler, GoHome
from unit5 import Blogjson
from unit4 import SignUp, Login, Logout, Welcome
from unit3 import Blog, NewPost, Post, Posts
from google.appengine.ext import db

from google.appengine.api import memcache

CACHE = {}

def front_page(update = False):
    key = 'front'
    blog = memcache.get(key)
    if not update and key in CACHE:
        blog = CACHE[key]
    else:
        logging.error('DB GOT the QUERY')
        blog = db.GqlQuery("SELECT * "  # Spaces at the end are important
                           "FROM Posts "
                           # "WHERE ANCESTOR IS :1 "
                           "ORDER BY created DESC "
                           "LIMIT 10")
        blog = list(blog)
        memcache.set(key, blog)
    return blog
# class Blogjson(Handler):
#     template = 'blog.json'
#     def get(self, post_id=''):
#         d = []
#         one_post = post_id.isdigit() and Posts.get_by_id(int(post_id))
#         if one_post:
#             self.initial_values['posts'] = [one_post]
#         else: self.initial_values['posts'] = Posts.all().order('-created')
#         for post in self.initial_values['posts']:
#             d.append({'content': post.content,
#                       'subject': post.subject})
#         self.render_json(d)
#
#     def render_json(self, d):
#         json_text = json.dumps(d)
#         self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
#         self.write(json_text)




app = webapp2.WSGIApplication([ ('/Unit6/?/?', Blog),
                                ('/Unit6//?(?:[Bb]log)?/?/?', Blog),
                                ('/Unit6/?(?:[Bb]log)?/newpost/?/?', NewPost),
                                ('/Unit6/?(?:[bB]log)?/(\d+)/?/?', Post),
                                ('/Unit6/?(?:[bB]log)?/?\.json/?', Blogjson),
                                ('/Unit6/?(?:[bB]log)?/(\d+)/?\.json/?', Blogjson),
                                ('/Unit6//?signup/?/?', SignUp),
                                ('/Unit6//?login/?/?', Login),
                                ('/Unit6//?logout/?/?', Logout),
                                ('/Unit6//?welcome/?/?', Welcome),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)