import webapp2, re

from handler import Handler, GoHome, Sitemodel
from google.appengine.ext import db
# import random, string
SECRET = 'whatev'


class Visits(Handler):
    def get(self, template='visits.html'):
        visits = self.readcookie('visits', default=0, numbered=True) + 1
        self.setcookie('visits', visits)
        self.renderjinja('visits.html', visits=visits)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

USERNAME_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
def invalid_username(un):

    if not (un or USERNAME_RE.match(un)):
        return 'That\'s not a valid username!'
    if Member.by_key(name=un):
        return 'That username already exists!'

class Member(Sitemodel):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    # def testprint(self):
    #     self.by_id('hello')


#
# @classmethod
# def by_id(cls, uid):
#         user = Member.get_by_id(uid)
#
#     @classmethod
#     def register(cls, name, password, email=None):
#         p = make_secure(password)
#         return cls(name=name, password_hash=p, email=email)

class SignUp(Handler):
    def renderSign(self, template='signupsecure.html', **params):
        self.renderjinja(template, **params)

    def get(self):
        self.renderSign()

    def post(self):
        username = self.name = self.request.get('username')
        password = self.password = self.request.get('password')
        verify = self.verify = self.request.get('verify')
        email = self.email = self.request.get('email')

        if not invalid_username(username) and password and password == verify and valid_email(email):
            email = ''
            self.setcookie('user', username)
            self.saveUser(username, password, email)
            self.redirect('/Unit4/welcome/')

        params = dict(username=username,
                      email=email)
        if invalid_username(username):
            params['invalidusername'] = invalid_username(username)
        if not password:
            params['invalidpassword'] = 'Password can\'t be empty!'
        if not valid_email(email):
            params['invalidemail'] = "This email is not a valid email."
        if password != verify:
            params['invalidverify'] = 'Password must match!'
        self.renderSign(**params)

    def saveUser(self, name, password, email=''):
        password_hash = self.hash_password(password)
        User = Member(name=name, password_hash=password_hash, email=email)
        User.put()

class Login(SignUp):
    def get(self):
        self.renderSign('login.html')

    def post(self):
        pass

class Welcome(SignUp):
    def get(self):
        user = self.readcookie('user')
        if not user:
            self.redirect('/Unit4/signup/')
        self.renderSign('welcome.html', name=user)


app = webapp2.WSGIApplication([('/Unit4/Visits/?', Visits),
                               ('/Unit4/signup/?', SignUp),
                               ('/Unit4/welcome/?', Welcome),
                               ('/Unit4/?', SignUp),
                               ('/Unit4/login/?', Login),
                               ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)