import json, requests, pymysql.cursors, telegram, os
from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename

config = json.load(open('config.json'))
tg_token = config['bot']['telegram']['token']


# Flask App and Telegram Bot
app = Flask(__name__)
bot = telegram.Bot(tg_token)


# Production connect
host = '80.211.177.35' if app.debug else config['db']['host']
db = pymysql.connect(
		host=host,
		user=config['db']['user'],
		password=config['db']['password'],
		db=config['db']['db'],
		cursorclass=pymysql.cursors.DictCursor)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'src/uploads/'


# Modules
import src.dbapi
import src.qr
import src.redirects

# ROUTES
@app.route("/", methods=['GET'])
def index():
	if 'peppuz' not in request.cookies and not app.debug:
		# Processing IP
		ip = requests.get('http://ip-api.com/json/%s' % request.remote_addr).json()
		text = "%s GET index\nFrom %s, %s, %s " % (request.remote_addr, ip['city'], ip['regionName'], ip['countryCode'])

		# DB INSERT
		with db.cursor() as cursor:
		    # Create a new record
		    sql = "INSERT INTO `connections` (`ip`, `citta`, `stato`, `date`) VALUES (%s, %s, %s, %s)"
		    cursor.execute(sql, (request.remote_addr, ip['city'], ip['countryCode'], str(datetime.now()) ) )
		db.commit()

		# Telegram Alert
		if ip['countryCode'] == 'IT':
			bot.send_message(config['bot']['telegram']['peppuz'],text)

	return render_template('index.html')


@app.route("/stampa", methods=['GET'])
def print_this():
	return redirect(url_for('uploaded_file', filename='print_this.pdf'))

@app.route('/download/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename=filename)

@app.route("/sure", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
