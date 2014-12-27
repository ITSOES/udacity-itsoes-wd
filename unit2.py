import webapp2
from handler import Handler, GoHome


class ShoppingList(Handler):
    template = 'shopping_list.html'
    def get(self):
        food = self.request.get_all("food")
        something = self.request.get("food")
        # print('                              here\'s the food', str(something), 'food', food)
        self.renderjinja(something=something, food=food)

class FizzBuzz(Handler):
    template = 'fizzbuzz.html'
    def get(self):
        n = self.request.get('n')
        n = n.isdigit() and int(n) # Returns int(n) if n.isdigit() is True
        self.renderjinja(n=n)

app = webapp2.WSGIApplication([ ('/Unit2/ShoppingList', ShoppingList),
                                ('/Unit2/FizzBuzz', FizzBuzz),
                                ('.*', GoHome)  # Any junk urls goes to the homepage
                              ], debug=True)
