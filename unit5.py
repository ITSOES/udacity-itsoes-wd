import webapp2
import urllib2, json
from xml.dom import minidom


from handler import Handler, GoHome
from unit4 import SignUp, Login, Logout, Welcome
from unit3 import Blog, NewPost, Post, Posts
# from google.appengine.ext import db




class Blogjson(Handler):
    template = 'blog.json'
    def get(self, post_id=''):
        d = []
        one_post = post_id.isdigit() and Posts.get_by_id(int(post_id))
        if one_post:
            self.initial_values['posts'] = [one_post]
        else: self.initial_values['posts'] = Posts.all().order('-created')
        for post in self.initial_values['posts']:
            d.append({'content': post.content,
                      'subject': post.subject})
        self.render_json(d)

    def render_json(self, d):
        json_text = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_text)




app = webapp2.WSGIApplication([ ('/Unit5/?/?', Blog),
                                ('/Unit5//?(?:[Bb]log)?/?/?', Blog),
                                ('/Unit5/?(?:[Bb]log)?/newpost/?/?', NewPost),
                                ('/Unit5/?(?:[bB]log)?/(\d+)/?/?', Post),
                                ('/Unit5/?(?:[bB]log)?/?\.json/?', Blogjson),
                                ('/Unit5/?(?:[bB]log)?/(\d+)/?\.json/?', Blogjson),
                                ('/Unit5//?signup/?/?', SignUp),
                                ('/Unit5//?login/?/?', Login),
                                ('/Unit5//?logout/?/?', Logout),
                                ('/Unit5//?welcome/?/?', Welcome),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)


# d = urllib2.urlopen('http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml')
# c = minidom.parseString(d.read())
# # print(c.toprettyxml())
#
# print(len(c.getElementsByTagName('item')))