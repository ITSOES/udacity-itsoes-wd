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


class Member(db.Model):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.EmailProperty()


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
        name = self.name = self.request.get('name')
        password = self.password = self.request.get('password')
        verify = self.verify = self.request.get('verify')
        email = self.email = self.request.get('email')

        if name and password and password == verify and valid_email(email):
            self.setcookie('user', name)
            self.redirect('/Unit4/Welcome/')

        params = dict(name=name,
                      email=email)
        if not password:
            params['invalidpassword'] = 'Password can\'t be empty'
        if not valid_email(email):
            params['invalidemail'] = "This email is not a valid email."
        if password != verify:
            params['invalidverify'] = 'Password must match'
        self.renderSign(**params)

    def saveUser(self, name, hash):
        pass


class Welcome(SignUp):
    def get(self):
        user = self.readcookie('user')
        if not user:
            self.redirect('/Unit4/SignUp/')
        self.renderSign('welcome.html', name=user)


app = webapp2.WSGIApplication([('/Unit4/Visits/?', Visits),
                               ('/Unit4/SignUp/?', SignUp),
                               ('/Unit4/Welcome/?', Welcome),
                               ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)