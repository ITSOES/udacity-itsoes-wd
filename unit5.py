import webapp2
import urllib2, json
from xml.dom import minidom


from handler import Handler, GoHome, Sitemodel
from unit3 import Blog, NewPost, Post
from google.appengine.ext import db




# class MyAPI(Handler):
#
#     def get(self):
#         self.renderjinja()




app = webapp2.WSGIApplication([ ('/Unit5/blog/?', Blog),
                                ('/Unit5/blog/newpost', NewPost),
                                ('/Unit5/[bB]log/(\d+)', Post),
                                ('/Unit5/blog/?\.json', Blog),
                                ('/Unit5/[bB]log/(\d+)/?\.json', Post),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)


# d = urllib2.urlopen('http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml')
# c = minidom.parseString(d.read())
# # print(c.toprettyxml())
#
# print(len(c.getElementsByTagName('item')))