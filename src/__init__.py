import json, requests, pymysql.cursors
import telegram
from flask import Flask, redirect, url_for, request, render_template, jsonify

config = json.load(open('config.json'))
tg_token = config['bot']['telegram']['token']


# Flask App and Telegram Bot
app = Flask(__name__)
bot = telegram.Bot(tg_token)

import src.redirects
import src.qr
import src.fdd

connection = pymysql.connect(
		host=config['db']['host'],
		user=config['db']['user'],
		password=config['db']['password'],
		db=config['db']['db'],
		cursorclass=pymysql.cursors.DictCursor)
	# EXAMPLE MYSQL
	# try:
	#     with connection.cursor() as cursor:
	#         # Create a new record
	#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
	#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
	#
	#     # connection is not autocommit by default. So you must commit to save
	#     # your changes.
	#     connection.commit()
	#
	#     with connection.cursor() as cursor:
	#         # Read a single record
	#         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
	#         cursor.execute(sql, ('webmaster@python.org',))
	#         result = cursor.fetchone()
	#         print(result)
	# finally:
	#     connection.close()
app.config['UPLOAD_FOLDER'] = 'src/uploads/'


# ROUTES
@app.route("/", methods=['GET'])
def index():
	if 'peppuz' not in request.cookies and not app.debug:
		# returns a json with all IP info
		ip = requests.get('http://ip-api.com/json/%s' % ip).json()
		text = "%s GET index\nFrom %s, %s, %s " \
			% (request.remote_addr, ip['city'], ip['regionName'], ip['countryCode'])
		bot.send_message(config['bot']['telegram']['peppuz'],text)
		# For the bot only send_message is allowed
		# otherwise other updaters will conflict
		# and the bot won't respond to any requests
	return render_template('index.html')
