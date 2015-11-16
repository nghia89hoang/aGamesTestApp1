from authomatic.provider import oauth2, openid, gaeopenid

CONFIG = {
	'fb': {
		'class' : oauth2.Facebook,
		'consumer_key' : '',
		'consumer_secret': '',
		'scope': ['user_about_me', 'email', 'publish_stream', 'read_stream']
	}
}