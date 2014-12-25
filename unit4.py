import webapp2, re
import hmac
from handler import Handler, GoHome
from google.appengine.ext import db
# import random, string
SECRET = 'whatev'


def hasher(s):
    return hmac.new(SECRET, str(s)).hexdigest()

def make_secure(s):
    return '%s|%s' % (str(s), hasher(s))

def check_secure_val(sHASH):
    s = sHASH.split('|')[0]
    return sHASH == make_secure(s) and s or 0

class Visits(Handler):
    def get(self, template='visits.html'):
        visit_cookie_val = self.request.cookies.get('visits')
        visits = visit_cookie_val and int(check_secure_val(visit_cookie_val)) + 1
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % make_secure(visits))
        self.renderjinja('visits.html', **{
            'visits': visits,
            })

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Member(db.Model):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.EmailProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        user = Member.get_by_id(uid)

    @classmethod
    def register(cls, name, password, email=None):
        p = make_secure(password)
        return cls(name=name, password_hash=p, email=email)

class SignUp(Handler):
    def renderSign(self, template='signupsecure.html',
                   name='',
                   email='',
                   invaliduser_error='',
                   invalidverify='',
                   invalidemail=''
                   ):
        self.renderjinja(template,
                         name=name,
                         email=email,
                         invaliduser_error=invaliduser_error,
                         invalidverify=invalidverify,
                         invalidemail=invalidemail)
    def get(self):
        self.renderSign()

    def post(self):
        name = self.name = self.request.get('name')
        password = self.password = self.request.get('password')
        verify = self.verify = self.request.get('verify')
        email = self.email = self.request.get('email')
        if name and password and password == verify and valid_email(email):
            self.response.headers.add_header('Set-Cookie',
                                             'user=%s; Path=/' % make_secure(name))
            self.redirect('/Unit4/Welcome/')

        params = dict(name =name,
                      email = email)
        if not valid_email(email):
            params['invalidemail'] = "This email is not a valid email."
        if password != verify:
            params['invalidverify'] = 'Password must match'
        self.renderSign(**params)

class Welcome(SignUp):
    def get(self):
        user_cookie_val = self.request.cookies.get('user')
        user = user_cookie_val and check_secure_val(user_cookie_val)
        if not user:
            self.redirect('/Unit4/SignUp/')
        self.renderSign('welcome.html', name=user)

app = webapp2.WSGIApplication([ ('/Unit4/Visits/?', Visits),
                                ('/Unit4/SignUp/?', SignUp),
                                ('/Unit4/Welcome/?', Welcome),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)