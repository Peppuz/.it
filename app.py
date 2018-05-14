import json, os, ftplib, requests, glob
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename

config = json.load(open('config.json'))
print(config)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# ROUTES
@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/spendTheCash")
def pricing():
	pass
	# return render_template('pricing.html')

# REDIRECTS
@app.route("/twitter")
def twitter():
	return redirect('https://twitter.com/zuppep')

@app.route("/tracks")
def soundcloud():
	return redirect(url_for('https://soundcloud.com/peppuz/tracks'))

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
@app.route("/fdd/upload", methods=['POST', 'GET'])
def fdd_attivita():
	"""
		* takes the POST data
		* adds new buttons to attivita
		* generates new Files to upload with fdd_upload(page)
	"""
	if not request.form and request.method is not 'POST':
		return render_template('admin.html')
	else:
		return render_request(request.form.copy(), request.files)

@app.route("/fdd/editoriale", methods=['POST', 'GET'])
def fdd_editoriale():
	if not request.form and request.method is not 'POST':
		return render_template('fdd_editoriale.html')
	else:
		return render_editoriale(request.form.copy(), request.files)

@app.route("/fdd/danilodolci", methods=['POST', 'GET'])
def fdd_dd():
	return jsonify(request.form)


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
		url.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		# Append JSON
		buttons.append({"title": button_title, "url":'http://%s/attivita/%s'%(host, filename)})
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
	for anno in input:
		if anno['anno'] is year:
			anno['content'].insert(0,{"titolo":title, "url":"attivita/%s.html" % title})
			boole = True

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
		ftp.storlines("STOR %s" % file , open('%s' % file, 'rb'))

	return redirect('http://localhost/fdd/attivita.html')


def render_editoriale(form):
	return
