import webapp2

class RootHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world, this is RootHandler.py')

app = webapp2.WSGIApplication([
    ('/', RootHandler),
], debug=True)