import json, os, ftplib, requests, glob, qrcode
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# ROUTES
@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/<input>", methods=['GET'])
def inline_search(input=None):
	if not input:
		return render_template('index.html')
	else:
		return redirect('http://ddg.gg/?q='+input)

@app.route("/curriculum")
def cv():
	return render_template('curriculum.html')
	# return render_template('pricing.html')

@app.route('/qr', methods=['POST', 'GET'])
def qrgen():
	if request.method == 'POST' and request.form:
		data = request.form['qr']
		qr = qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4)
		qr.add_data(data)
		qr.make(fit=True)
		img = qr.make_image(fill_color="black", back_color="transparent")
		img.save(open("static/qr/%s.png"%data,'wb'))

		img = "qr/%s.png" % data
		return render_template('qr.html', data=data, img=img)
	return render_template('qr.html')


@app.route('/qr/<data>')
def qr(data=None):
	if not data:
		render_template('index.html')

	qr = qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_L,
	    box_size=10,
	    border=4)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(back_color="transparent")
	img.save(open("static/qr/%s.png"%data,'wb'))

	img = "qr/%s.png" % data
	return render_template('qr.html', data=data, img=img)


@app.route('/takeplace')
def takeplace():
	# TODO: Slack alert integration
	# request.remote_addr
	return render_template('takeplace.html')


# REDIRECTS
@app.route("/twitter")
def twitter():
	return redirect('https://twitter.com/zuppep')

@app.route("/tracks")
def soundcloud():
	return redirect('https://soundcloud.com/peppu_z/tracks')

@app.route("/fb")
def facebook():
	return redirect('https://facebook.com/p3ppu')

@app.route("/ig")
def instagram():
	return redirect("https://instagram.com/peppuz_")

@app.route("/tg")
def telegram():
	return redirect('https://t.me/peppu_z')

@app.route("/2stoned")
def youtube2():
	return redirect('https://ddg.gg')


# DemCar redirect
@app.route('/dc')
@app.route('/demcar')
def demcar():
	return redirect("http://demcar.it")

# Fondo Danilo Dolci redirect
@app.route("/fdd")
@app.route("/fondodanilodolci")
def fdd():
	return redirect("http://fondodanilodolci.it")

# Fondo Danilo Dolci login
@app.route("/fdd/login", methods=['GET', 'POST'])
def fdd_login():
	"""
		* Checks if posted data is correct
	"""
	if request.method == 'POST' and request.form['pwd'] == 'password':
		return redirect(url_for('fdd_select'))
	else:
		return render_template('fdd_login.html')

@app.route('/fdd/select')
def fdd_select():
	return render_template('fdd_select.html')

# Fondo Danilo Dolci Generator & Uploder static pages
@app.route("/fdd/attivita", methods=['POST', 'GET'])
def fdd_attivita():
	"""
		* takes the POST data
		* adds new buttons to attivita
		* generates new Files to upload with fdd_upload(page)
	"""
	if not request.form and request.method is not 'POST':
		return render_template('fdd_attivita.html')
	else:
		for key in request.form:
			if request.form[key] is '':
				return render_template('fdd_error.html')
		return render_request(request.form.copy(), request.files)

@app.route("/fdd/editoriale", methods=['POST', 'GET'])
def fdd_editoriale():
	if not request.form and request.method is not 'POST':
		return render_template('fdd_editoriale.html')
	else:
		for key in request.form:
			if request.form[key] is '':
				return render_template('fdd_error.html')
		return render_editoriale(request.form.copy(), request.files)

@app.route("/fdd/danilodolci", methods=['POST', 'GET'])
def fdd_dd():
	if not request.form and request.method is not 'POST':
		return render_template('fdd_dd.html')
	else:
		for key in request.form:
			if request.form[key] is '':
				return render_template('fdd_error.html')
		return render_dd(request.form.copy(), request.files)


def render_request(form, files):
	# FTP login
	host = "localhost"
	user = "Peppuz"
	pwd = "C"
	ftp = ftplib.FTP(host)
	ftp.login(user, pwd)
	ftp.cwd('/Applications/MAMP/htdocs/fdd/attivita')

	# Getting and removing title and year
	title = form['title']
	year = form['year']
	del form['title']
	del form['year']

	buttons = []
	count = 0
	# Output di questo while e' il Buttons (JSON) per evento
	while form:
		button_title = form.get('buttons-%s' % count)
		url = files.get('url-%s' % count)
		filename = secure_filename(url.filename)

		# Saving local
		try:
			url.save('uploads/'+filename)
		except Exception as e:
			url.save(filename)

		# Append JSON
		buttons.append({"title": button_title, "url":'http://%s/fdd/attivita/%s'%(host, filename)})
		del form['buttons-%s' % count]
		count += 1

	# Generating Event js
	part1 = open('static/fdd/template_evento.html').read()
	part2 = open('static/fdd/template_evento2.html').read()
	new_data = "var currentPosition = '%s';\
	inHTML('jumbotron', currentPosition);inHTML('head_title', currentPosition + ' | Fondo Danilo Dolci');\
	let data = %s ;" % (title, json.dumps(buttons))

	# Attivita update
	input = requests.get("http://localhost/fdd/attivita.json").json()
	boole = False
	date = []

	for key in input:
		if year == key.get('anno') or int(year) == key.get('anno'):
			key["content"].insert(0,{"titolo":title, "url":"attivita/%s.html" % title})
			boole = True
			break
	if not boole:
		input.insert(0, {"anno":year, "content":[{"titolo":title, "url":"attivita/%s.html" % title }]})

	input = json.dumps(input)

	# Creating Files to Upload
	with open('uploads/attivita.json', 'w') as target:
		target.write(input)

	with open('uploads/%s.html' % title, 'w') as target:
		target.write(part1+new_data+part2)

	# Upload Attivita
	ftp.cwd('/Applications/MAMP/htdocs/fdd')
	ftp.storlines("STOR attivita.json" , open('uploads/attivita.json', 'rb'))
	os.remove(app.config['UPLOAD_FOLDER']+'attivita.json')

	# Upload evento html
	ftp.cwd('/Applications/MAMP/htdocs/fdd/attivita')
	ftp.storlines("STOR %s.html" % title , open('uploads/%s.html' % title, 'rb'))
	os.remove('%s%s.html'% (app.config['UPLOAD_FOLDER'], title))

	# Upload files in attivita
	os.chdir(app.config['UPLOAD_FOLDER'])
	for file in glob.glob("*.*"):
		ftp.storbinary("STOR %s" % file , open('%s' % file, 'rb'))
		os.remove(file)
	ftp.close()
	os.chdir('../')

	return redirect('http://localhost/fdd/attivita.html')

def render_editoriale(form, files):
	# FTP login
	host = "localhost"
	user = "Peppuz"
	pwd = "C"
	ftp = ftplib.FTP(host)
	ftp.login(user, pwd)
	ftp.cwd('/Applications/MAMP/htdocs/fdd/editoriale')

	# Getting and removing title and year
	title = form['title']
	year = form['year']
	del form['title']
	del form['year']

	buttons = []
	count = 0
	# Output di questo while e' il Buttons (JSON) per evento
	while form:
		button_title = form.get('buttons-%s' % count)
		url = files.get('url-%s' % count)
		filename = secure_filename(url.filename)

		# Saving local
		try:
			url.save('uploads/'+filename)
		except Exception as e:
			url.save(filename)

		# Append JSON
		buttons.append({"title": button_title, "url":'http://%s/fdd/editoriale/%s'%(host, filename)})
		del form['buttons-%s' % count]
		count += 1

	# Generating Event js
	part1 = open('static/fdd/template_evento.html').read()
	part2 = open('static/fdd/template_evento2.html').read()
	new_data = "var currentPosition = '%s';\
	inHTML('jumbotron', currentPosition);inHTML('head_title', currentPosition + ' | Fondo Danilo Dolci');\
	let data = %s ;" % (title, json.dumps(buttons))

	# Attivita update
	input = requests.get("http://localhost/fdd/editoriale.json").json()
	boole = False

	for key in input:
		if year == key.get('anno') or int(year) == key.get('anno'):
			key["content"].insert(0,{"titolo":title, "url":"editoriale/%s.html" % title})
			boole = True
			break
	if not boole:
		input.insert(0, {"anno":year, "content":[{"titolo":title, "url":"editoriale/%s.html" % title }]})

	input = json.dumps(input)

	# Creating Files to Upload
	with open('uploads/editoriale.json', 'w') as target:
		target.write(input)

	with open('uploads/%s.html' % title, 'w') as target:
		target.write(part1+new_data+part2)

	# Upload Attivita
	ftp.cwd('/Applications/MAMP/htdocs/fdd')
	ftp.storlines("STOR editoriale.json" , open('uploads/editoriale.json', 'rb'))
	os.remove(app.config['UPLOAD_FOLDER']+'editoriale.json')

	# Upload evento html
	ftp.cwd('/Applications/MAMP/htdocs/fdd/editoriale')
	ftp.storlines("STOR %s.html" % title , open('uploads/%s.html' % title, 'rb'))
	os.remove('%s%s.html'% (app.config['UPLOAD_FOLDER'], title))

	# Upload files in attivita
	os.chdir(app.config['UPLOAD_FOLDER'])
	for file in glob.glob("*.*"):
		ftp.storbinary("STOR %s" % file , open('%s' % file, 'rb'))
		os.remove(file)
	ftp.close()
	os.chdir('../')

	return redirect('http://localhost/fdd/editoriale.html')

def render_dd(form, files):
	# FTP login
	host = "localhost"
	user = "Peppuz"
	pwd = "C"
	ftp = ftplib.FTP(host)
	ftp.login(user, pwd)
	ftp.cwd('/Applications/MAMP/htdocs/fdd/')

	buttons = []
	count = 0
	# Output di questo while e' il Buttons (JSON) per evento
	while form:
		button_title = form.get('buttons-%s' % count)
		url = files.get('url-%s' % count)
		filename = secure_filename(url.filename)

		# Saving local
		try:
			url.save('uploads/'+filename)
		except Exception as e:
			url.save(filename)

		# Append JSON
		buttons.append({"title": button_title, "url":'http://%s/fdd/danilodolci/%s'%(host, filename)})
		del form['buttons-%s' % count]
		count += 1

	input = requests.get("http://localhost/fdd/dd.json").json()
	boole = False

	input += buttons
	input = json.dumps(input)


	with open('uploads/dd.json', 'w') as target:
		target.write(input)

	ftp.storlines("STOR dd.json" , open('uploads/dd.json', 'rb'))

	os.remove(app.config['UPLOAD_FOLDER']+'dd.json')

	ftp.cwd('/Applications/MAMP/htdocs/fdd/danilodolci')

	os.chdir(app.config['UPLOAD_FOLDER'])
	for file in glob.glob("*.*"):
		ftp.storbinary("STOR %s" % file , open('%s' % file, 'rb'))
		os.remove(file)
	ftp.close()
	os.chdir('../')

	return redirect('http://localhost/fdd/Danilo-Dolci.html')
