from src import app
from flask import redirect, render_template, request, send_from_directory, jsonify
import qrcode, urllib.parse

# QR Generator
@app.route('/qr', methods=['POST', 'GET'])
def qrgen():
	if request.method == 'POST' and request.form:
		data = request.form['qr']

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4)
		qr.add_data(data)
		qr.make(fit=True)

		filename = urllib.parse.quote_plus(data)

		img = qr.make_image(fill_color="black", back_color="transparent")
		img.save(open("src/static/qr/%s.png" % filename,'wb'))
		img = "qr/%s.png" % filename

		return render_template('qr.html', data=data, img=img)
	return render_template('qr.html')

@app.route('/qr/<data>')
def qr(data=None):
	if not data:
		render_template('qr.html')
		
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
	return send_from_directory('static', img)
