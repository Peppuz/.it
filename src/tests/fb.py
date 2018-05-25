import requests

token ="cc96c16238097cab7728bb51d1afe8c6"
post = 'Orari STP 4 Test Flask Backend'
post.replace(' ', '+')
try:
	requests.post("https://graph.facebook.com/me/feed/?message=" + post + "&access_token=" + token)
except Exception as e:
	raise e
