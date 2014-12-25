import webapp2
from handler import Handler, GoHome


class Homepage(Handler):
    def get(self):
        self.renderjinja('Homepage.html')

app = webapp2.WSGIApplication([ ('/', Homepage),
                                ('.*', GoHome)
                              ], debug=True)
