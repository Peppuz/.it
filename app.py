from flask import Flask, abort, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ROUTES
@app.route("/", methods=['GET'])
def index():
	print request 
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

@app.route("/2stoned")
def youtube2():
	return redirect('https://ddg.gg')

@app.route("/fdd", methods=['POST', 'GET'])
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
	return  "problem solved"

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

 	# return render_template('index.html')
