import webapp2, logging
from handler import Handler, GoHome, Sitemodel
from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import datetime, timedelta

# blog_key = db.Key.from_path('Posts', 'key')
print('HIHIH')  # dsf
def multi_memcache_get(*keys):
    result = {key: '' for key in keys}
    result.update(memcache.get_multi(keys))
    return [result[key] for key in keys]


last_all_queried = memcache.get('last all queried')
last_queried = ''
# print(last_queried, 'is there anything here?')
def front_page(update=False, post_id=''):
    global last_queried, last_all_queried
    # post = ''
    if post_id:

        last_queried, post = multi_memcache_get('LQ' + str(post_id), str(post_id))
        # print(last_queried, 'sdfasdfasdfeWEWQERQWEREWQR', post)
        if not (last_queried and post):
            # print('DB Q\'ed for single post', last_queried)
            last_queried, post = datetime.today(), Posts.by_id(post_id)
            # memcache.set('LQ' + str(post_id), last_queried)
            # memcache.set(str(post_id), post)
            memcache.set_multi({'LQ' + str(post_id): last_queried,
                                       str(post_id): post})
            return post
        else:
            return post

    key = 'front'
    blog = memcache.get(key)
    if not all([last_all_queried, not update, blog]):
        last_all_queried = datetime.today()
        memcache.set('last all queried', last_all_queried)
        logging.error('DB GOT the QUERY')
        blog = db.GqlQuery("SELECT * "
                           "FROM Posts "
                           "ORDER BY created DESC "
                           "LIMIT 10")
        blog = list(blog)
        memcache.set(key, blog)
    return blog


class Posts(Sitemodel):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)

class Blog(Handler):
    template = 'blog.html'
    initial_values = {
        'posts': front_page(),  # Posts.all().order('-created')
        'last_queried': lambda: round((datetime.today() - last_all_queried).total_seconds(), 1)
    }

class Post(Blog):
    template = 'singlepost.html'
    initial_values = {
        'post': '',
        'last_queried': lambda: round((datetime.today() - last_queried).total_seconds(), 1)
    }

    def get(self, post_id):
        # logging.debug('DATABASEg BY ID')
        # print('DATA BASE BY ID', last_queried)
        post = post_id.isdigit() and front_page(post_id=int(post_id))
        print(post, "ASDFWAWWWW")
        if not post:
            self.error(404)
            self.redirect('/Unit5/Blog')
            return
        # if json:
        #     self.render
        self.renderjinja(subject=post.subject, content=post.content)


class NewPost(Handler):
    template = 'newpost.html'

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

class Flush(Handler):
    def get(self):
        global last_all_queried
        memcache.flush_all()
        self.redirect('/Unit5/')
        last_all_queried = datetime.today()

app = webapp2.WSGIApplication([('/Unit3/Blog/?', Blog),
                               ('/Unit3/Blog/newpost', NewPost),
                               ('/Unit3/Blog/(\d+)', Post),
                               ('/Unit3/flush', Flush),
                               ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)