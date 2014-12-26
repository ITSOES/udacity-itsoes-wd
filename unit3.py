import webapp2
from handler import Handler, GoHome, Sitemodel
from google.appengine.ext import db

class Blog(Handler):
    def render_front(self, template='blog.html',
                     subject='',
                     content='',
                     error=''):
        posts = Posts.all().order('-created')

        self.renderjinja(template, **{
            'subject':  subject,
            'content':  content,
            'error':    error,
            'posts':    posts
        })

    def get(self):
        pass
        self.render_front()

class Posts(Sitemodel):

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    # created = db.DateTimeProperty(auto_now_add=True)

class Post(Blog):
    def get(self, post_id):
        post = post_id.isdigit() and Posts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            self.redirect('/Unit3/Blog')
            return
        self.render_front(template='singlepost.html', subject=post.subject, content=post.content)

class NewPost(Blog):
    def get(self):
        pass
        self.renderjinja('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        # print(content)
        if not (subject and content):
            error = 'We need both a subject and some post content.'
            self.render_front(template='newpost.html', subject=subject, content=content, error=error)
        else:
            a = Posts(subject=subject, content=content)
            a.put()
            self.redirect('/Unit3/Blog/%d' % a.key().id())

app = webapp2.WSGIApplication([ ('/Unit3/Blog/?', Blog),
                                ('/Unit3/Blog/newpost', NewPost),
                                ('/Unit3/Blog/(\d+)', Post),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)