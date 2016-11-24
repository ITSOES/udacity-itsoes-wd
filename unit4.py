import webapp2
import re

from handler import Handler, GoHome, Sitemodel
from google.appengine.ext import db
SECRET = 'whatev'


class Visits(Handler):
    template = 'visits.html'
    def get(self):
        visits = self.readcookie('visits', default=0, numbered=True) + 1
        self.setcookie('visits', visits)
        self.renderjinja(visits=visits)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)


USERNAME_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')


def invalid_username(un):
    if not (un or USERNAME_RE.match(un)):
        return 'That\'s not a valid username!'
    if Member.by_key(name=un):
        return 'That username already exists!'
    return ''


class Member(Sitemodel):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=False)


class SignUp(Handler):
    template = 'signupsecure.html'

    def initialize(self, *a, **kw):
        # I'm aware that the following code does not check the Google
        # datastore for the user
        super(Handler, self).initialize(*a, **kw)
        self.user = self.readcookie('user')

    # def renderSign(self, **params):
    #     self.renderjinja(**params)

    # def get(self):
    #     self.renderSign()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not invalid_username(username) and password and password == verify and valid_email(email):
            email = ''
            self.setcookie('user', username)
            self.saveUser(username, password, email)
            self.redirect('/Unit5/welcome/')
            return

        params = dict(username=username,
                      email=email)
        params['invalidusername'] = invalid_username(username)
        if not password:
            params['invalidpassword'] = 'Password can\'t be empty!'
        if not valid_email(email):
            params['invalidemail'] = "This email is not a valid email."
        if password != verify:
            params['invalidverify'] = 'Password must match!'
        self.renderjinja(**params)

    def saveUser(self, name, password, email=''):
        password_hash = self.hash_password(password)
        User = Member(name=name, password_hash=password_hash, email=email)
        User.put()


class Login(SignUp):
    template = 'login.html'

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = Member.by_key(name=username)
        if u and self.hash_password(password) == u.password_hash:
            self.setcookie('user', username)
            self.redirect('/Unit5/welcome')
            return
        params = dict(username=username, invalidusername='Invalid user or password')
        self.renderjinja(**params)


class Logout(SignUp):
    def get(self):
        self.setcookie('user', '')
        self.redirect('/Unit5/signup')



class Welcome(SignUp):
    template = 'welcome.html'
    def get(self):
        if not self.user:
            self.redirect('/Unit5/signup/')
        self.renderjinja(name=self.user)


app = webapp2.WSGIApplication([('/Unit4/Visits/?', Visits),
                               ('/Unit4/signup/?', SignUp),
                               ('/Unit4/welcome/?', Welcome),
                               ('/Unit4/?', SignUp),
                               ('/Unit4/login/?', Login),
                               ('/Unit4/logout/?', Logout),
                               ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)