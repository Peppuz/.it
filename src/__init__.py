import json, requests, pymysql.cursors, telegram
from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify

config = json.load(open('config.json'))
tg_token = config['bot']['telegram']['token']


# Flask App and Telegram Bot
app = Flask(__name__)
bot = telegram.Bot(tg_token)

# Modules
import src.redirects
import src.qr
import src.fdd

# Production connect
if not app.debug:
	connection = pymysql.connect(
			host=config['db']['host'],
			user=config['db']['user'],
			password=config['db']['password'],
			db=config['db']['db'],
			cursorclass=pymysql.cursors.DictCursor)
app.config['UPLOAD_FOLDER'] = 'src/uploads/'


# ROUTES
@app.route("/", methods=['GET'])
def index():
	if 'peppuz' not in request.cookies and not app.debug:
		# Processing IP
		ip = requests.get('http://ip-api.com/json/%s' % ip).json()
		text = "%s GET index\nFrom %s, %s, %s " % (request.remote_addr, ip['city'], ip['regionName'], ip['countryCode'])

		# DB INSERT
		with connection.cursor() as cursor:
		    # Create a new record
		    sql = "INSERT INTO `connection` (`ip`, `citta`, `stato`, `date`) VALUES (%s, %s, %s, %s)"
		    cursor.execute(sql, (request.remote_addr, ip['city'], ip['countryCode'], str(datetime.now()) ) )
		connection.commit()

		# Telegram Alert
		bot.send_message(config['bot']['telegram']['peppuz'],text)

	return render_template('index.html')
