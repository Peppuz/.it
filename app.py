import json
from flask import Flask, abort, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename

config = json.load(open('config.json').read())
print config
app = Flask(__name__)

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

@app.route("/fdd/login", methods=['GET', 'POST'])
def fdd_login():
	"""
		* Checks if posted data is correct
	"""
	if request.method == 'POST':
		if request.form['usr'] == 'gigi' and request.form['pwd'] == '12345':
			session['username'] = request.form['username']
			return render_template('fdd_admin.html')
		else:
			redirect(url_for('fdd'))
	else:
		render_template('fdd_login.html')


# Fondo Danilo Dolci Generator & Uploder static pages
@app.route("/fdd/upload", methods=['POST', 'GET'])
def fondoDaniloDolci():
	"""
		* takes the POST data
		* adds new buttons to attivita
		* generates new Files to upload with fdd_upload(page)

	"""
	buttons = []
	title = ''
	year  = ''
	# TODO: add auto set Year from currentDate
	return  jsonify(request.form)
	if request.method == 'POST':
		for key, val in request.form:
			if key == 'title' and not val:
				return "Errore: non e' stato inserito alcun Titolo! <br> Torna indietro e ricompila il modulo correttamente."
			else:
				title = val
			if key == 'year' and not val:
				year = val
			# TODO: ADD button to array as Dictionary with title,url
			if key[0:7] == 'buttons-':
				# buttons.append(val)
				print("yes it works Now append something ")
	# r = request.args.get('note, '')
 	# return render_template('index.html')
