from src import app
from flask import redirect, render_template, request
import qrcode

# QR Generator
@app.route('/qr', methods=['POST', 'GET'])
def qrgen():
	if request.method == 'POST' and request.form:
		data = request.form['qr']
		if "/" in data:
			return render_template('qr.html', error="Slashes '/' are not allowed")

		qr = qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4)
		qr.add_data(data)
		qr.make(fit=True)
		img = qr.make_image(fill_color="black", back_color="transparent")
		img.save(open("src/static/qr/%s.png"%data,'wb'))

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
