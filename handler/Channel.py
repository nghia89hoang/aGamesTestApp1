import webapp2

class Channel(webapp2.RequestHandler):
  def get(self):
    self.response.write('GET handled');
    
  def post(self):
    self.response.write("POST handled: " + self.request.get("ChannelUri"));
    
app = webapp2.WSGIApplication([
    ('/channel', Channel)
], debug=True)