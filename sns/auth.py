import webapp2
import urllib

class SnsAuth(webapp2.RequestHandler):
  pass

app = webapp2.WSGIApplication([('/sns', SnsAuth)], debug=True)