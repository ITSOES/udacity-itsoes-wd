import webapp2
from handler import Handler, GoHome, Sitemodel
from google.appengine.ext import db

class Posts(Sitemodel):

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    # created = db.DateTimeProperty(auto_now_add=True)

class Blog(Handler):
    template = 'blog.html'
    initial_values = {
        'posts': Posts.all().order('-created')
    }

class Post(Handler):
    template = 'singlepost.html'
    # initial_values = {
    #     'subject': ''
    # }

    def get(self, post_id, json=False):
        # print(self.request.url)
        post = post_id.isdigit() and Posts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            self.redirect('/Unit3/Blog')
            return
        if json:
            self.render
        self.renderjinja(subject=post.subject, content=post.content)

class NewPost(Handler):
    template='newpost.html'

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if not (subject and content):
            error = 'We need both a subject and some post content.'
            self.renderjinja(subject=subject, content=content, error=error)
        else:
            a = Posts(subject=subject, content=content)
            a.put()
            self.redirect('/Unit5/%d/' % a.key().id())

class JsonBlog(Blog):
    template = 'jsonblog.xml'


app = webapp2.WSGIApplication([ ('/Unit3/Blog/?', Blog),
                                ('/Unit3/Blog/newpost', NewPost),
                                ('/Unit3/Blog/(\d+)', Post),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)