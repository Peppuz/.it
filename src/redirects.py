from src import app
from flask import redirect, render_template

@app.route("/<input>", methods=['GET'])
def inline_search(input=None):
	if not input:
		return render_template('index.html')
	else:
		return redirect('http://ddg.gg/?q='+input)

@app.route("/facebook")
@app.route("/fb")
def facebook():
	return redirect('https://facebook.com/p3ppu')

@app.route("/ig")
def instagram():
	return redirect("https://instagram.com/peppuz_")

@app.route("/tg")
@app.route("/telegram")
def telegram():
	return redirect('https://t.me/peppu_z')

@app.route("/gh")
@app.route("/github")
def github():
	return redirect('https://github.com/Peppuz')

@app.route('/webmail')
def aruba_mail():
	return redirect('https://webmail.aruba.it')

# DemCar redirect
@app.route('/demcar')
@app.route('/dc')
def demcar():
	return redirect("http://demcar.it")

@app.route("/twitter")
def twitter():
	return redirect('https://twitter.com/zuppep')

@app.route("/soundcloud")
@app.route("/sc")
@app.route("/tracks")
def soundcloud():
	return redirect('https://soundcloud.com/peppu_z/tracks')

@app.route('/takeplace')
@app.route('/tp')
def takeplace():
	# TODO: Slack alert integration
	# request.remote_addr
	return redirect('http://take-place.it')
