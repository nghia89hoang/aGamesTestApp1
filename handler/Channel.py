import webapp2
import urllib
import json
from google.appengine.api import urlfetch
from google.appengine.api import memcache

#s_client_secret = '2aU06eTD4M/1QFoIXN0Gelp+b8cJFIax'
s_client_secret = ''
s_client_id = ''
s_packageSID = ''
#s_channelUri = ''
#s_at = ''

class Channel(webapp2.RequestHandler):
  #def __init__(self):
    
  def get(self):    
    pushText = self.request.get("pT")    
    if pushText is not None and pushText != '':
      at = memcache.get('token')
      if at is not None:        
        self.response.write("Sending Push...")
        self.sendTextPush(pushText, at)
      else:
        self.response.write("\nAuthenticate failed!!")
    else:
    	self.response.write("Push what? "+ str(s_packageSID)  + "secret: "+ str(s_client_secret))
  def post(self):
    channelUri = self.request.get("ChannelUri")    
    memcache.set(key = "channelUri", value = channelUri)
    # TMP 
    #at = memcache.get('token')
    #if at is not None:
    self.getAT()
    #self.response.write("at existed " + at)    
    
  def getAT(self):
    url = 'https://login.live.com/accesstoken.srf'
    param = {
      "grant_type": "client_credentials",
      "client_id": s_packageSID,
      "client_secret": s_client_secret,
      "scope": "notify.windows.com"
    }
    e_param = urllib.urlencode(param)
    self.response.write(e_param)
    result = urlfetch.fetch(url = url,
                           payload = e_param,
                           method = urlfetch.POST,
                           headers = {'Content-Type': 'application/x-www-form-urlencoded',
                                     'Content-Length': str(len(e_param))})
    if result.status_code == 200:      
      jResult = json.loads(result.content)
      at = jResult.get('access_token')
      memcache.add(key = 'token', value = at)
      self.response.write("AT: " + at)
    else:
      self.response.write("WNS status code: " + str(result.content))
    

  def sendTextPush(self, txt, at):
    content = """<toast launch="">
              <visual lang="en-US">
                <binding template="ToastImageAndText01">
                  <image id="1" src="World" />
                  <text id="1">{TEXT}</text>
                </binding>
              </visual>
            </toast>"""
    content = content.replace("{TEXT}", txt)
    headers = {
      "Authorization": "Bearer " + str(at),
      "X-WNS-RequestForStatus": "true",
      "X-WNS-Type": "wns/toast",
      "Content-Type": "text/xml",
      "Content-Length": str(len(content)),
    }
    channelUri = memcache.get('channelUri')
    if channelUri is not None:
      self.response.write("ChanelURI :" + channelUri + "<br>")
      self.response.write("headers :" + str(headers) + "<br>")
      result = urlfetch.fetch(url = channelUri,
    	                        payload = content,
    	                        method = urlfetch.POST,
    	                        headers = headers)
      if result.status_code == 200:
        self.response.write("<br> PUSHED with content: " + txt)
      else:
        #device_stat = result.headers['X-WNS-DeviceConnectionStatus']
        err_desc = result.headers['X-WNS-Error-Description']
        msg_id = result.headers['X-WNS-Msg-ID']
        stat = result.headers['X-WNS-Status']
        self.response.write("<br> PUSH FAILED with code: " + str(result.status_code) + 
                            #" <br> deviceStat: " + str(device_stat) +
                            " <br> err Desc: " + str(err_desc) +
                            " <br> msg id: " + str(msg_id) +
                            " <br> stat: " + str(stat))
      
      
app = webapp2.WSGIApplication([
    ('/channel', Channel)
], debug=True)