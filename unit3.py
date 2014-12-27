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
        'subject':  '',
        'content':  '',
        'posts': Posts.all().order('-created')
    }
    # def render_front(self, **params):
    #
    #     # params
    #     params = dict(self.initial_values.items()
    #                   + params.items())
    #
    #     params['posts'] = Posts.all().order('-created')
    #
    #     self.renderjinja(**params)

    # def get(self):
    #     pass
    #     self.renderjinja()

class Post(Blog):
    template = 'singlepost.html'

    def get(self, post_id):
        post = post_id.isdigit() and Posts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            self.redirect('/Unit3/Blog')
            return
        self.renderjinja(subject=post.subject, content=post.content)

class NewPost(Blog):
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
            self.redirect('/Unit3/Blog/%d' % a.key().id())

class JsonBlog(Blog):
    template = 'jsonblog.xml'


app = webapp2.WSGIApplication([ ('/Unit3/Blog/?', Blog),
                                ('/Unit3/Blog/newpost', NewPost),
                                ('/Unit3/Blog/(\d+)', Post),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)