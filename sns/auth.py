import webapp2
import urllib
from authomatic import Authomatic
from authomatic.adapters import Webapp2Adapter
from config import CONFIG 

authomatic = Authomatic(config=CONFIG, secret='some random secret string')

class SnsAuth(webapp2.RequestHandler):
  def get(self)
    result = authomatic.login(Webapp2Adapter(self), 'fb')
    if result:
      self.response.write('l s')
app = webapp2.WSGIApplication([('/sns', SnsAuth)], debug=True)