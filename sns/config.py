from authomatic.provider import oauth2, openid, gaeopenid

CONFIG = {
	'fb': {
		'class' : oauth2.Facebook,
		'consumer_key' : '249629475103444',
		'consumer_secret': 'd24204ed6d5fe592ad63f2f856e46f07',
		'scope': ['user_about_me', 'email', 'publish_stream', 'read_stream']
	}
}