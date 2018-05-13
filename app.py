import json, os, ftplib, urllib.request
from flask import Flask, redirect, url_for, request, render_template, jsonify, flash
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
	if request.method == 'POST':
		if request.form['usr'] == config['fdd']['username'] and request.form['pwd'] == config['fdd']['password']:
			session['username'] = request.form['username']
			return render_template('fdd_admin.html')
		else:
			redirect(url_for('fdd'))
	else:
		return render_template('fdd_login.html')

# Fondo Danilo Dolci Generator & Uploder static pages
@app.route("/fdd/upload", methods=['POST', 'GET'])
def fondoDaniloDolci():
	"""
		* takes the POST data
		* adds new buttons to attivita
		* generates new Files to upload with fdd_upload(page)
	"""
	if not request.form and request.method is not 'POST':
		return render_template('admin.html')
	else:
		return render_request(request.form.copy(), request.files)


def render_request(form, files):
	title = form['title']
	year = currentYear if not form['year'] else form['year']
	buttons = []

	del form['title']
	del form['year']

	count = 0
	# Output di questo while e' il Buttons (JSON) per evento
	while form:
		title = form.get('buttons-%s' % count)
		url = files.get('url-%s' % count)
		filename = secure_filename(url.filename)

		# Saving
		url.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		# Append JSON
		buttons.append({"title": title, "url":'http://fondodanilodolci.it/attivita/'+filename})
		del form['buttons-%s' % count]
		count += 1


	''' Questo modulo genera HTML per l'evento '''
	# Generating Event
	part1 = open('static/fdd/template_evento.html').read()
	part2 = open('static/fdd/template_evento2.html').read()
	new_data = "var currentPosition = '%s';inHTML('jumbotron', currentPosition);inHTML('head_title', currentPosition + ' | Fondo Danilo Dolci');let data = %s ;" % (title, json.dumps(buttons))

	host = "localhost"
	user = "Peppuz"
	pwd = "C"

	# FTP login
	ftp = ftplib.FTP(host)
	ftp.login(user, pwd)
	ftp.cwd('/Applications/MAMP/htdocs/fdd/attivita')

	# Attivita update
	reach = "http://localhost/fdd/attivita.json"
	raw_data = urllib.request.urlopen(reach).read()
	input = json.loads(raw_data)
	input.insert(0, new_data)

	# Creating Files to Upload
	with open('uploads/attivita.json', 'w') as target:
		target.write(output)

	with open('uploads/%s.html' % title, 'w') as target:
		target.write(part1+new_data+part2)

	ftp.cwd('/Applications/MAMP/htdocs/fdd')
	ftp.storlines("STOR attivita.json" , open('uploads/attivita.json'))
	ftp.cwd('/Applications/MAMP/htdocs/fdd/attivita')
	ftp.storlines("STOR attivita.json" , open('uploads/%s.html' % title))

	return jsonify(buttons)

#  Attivita Year
# 	{
#     "anno":2014,
#     "content":[
#       {
#         "titolo":"III° PREMIO BIENNALE 2014 FONDO DANILO DOLCI PER LA LEGALITA’ E LA NONVIOLENZA IN MEMORIA DI PIERO BARIATI",
#         "url":"attivita/BandoBiennale2014.html"
#       },
#       { "titolo":"NUOVO BANDO FONDO DANILO DOLCI 2014", "url":"attivita/Bando2014.html"}
#
#     ]
#   },

# Evento
#   [
#     {title: 'Bando', url: 'http://fondodanilodolci.it/risorse/archivio/2007_BandoFDD.pdf'},
#     {title: 'Verbale', url: 'http://fondodanilodolci.it/risorse/archivio/2007_BandoFDD_verbale.pdf'},
#     {title: 'Premiazione', url: 'http://fondodanilodolci.it/risorse/archivio/2007_BandoFDD_assegnazione.pdf'},
#   ]
