from src import app
from flask import redirect, render_template, request, send_from_directory, jsonify
import qrcode
import urllib

# QR Generator
@app.route('/qr', methods=['POST', 'GET'])
def qr():
	if request.method == 'POST' and request.form:
		print request.form
		if request.form['name']:
			data = "BEGIN:VCARD \nVERSION:2.1\n"
			if request.form['name'] and request.form['surname']:
				data += "N:%s;%s\n" % (request.form['surname'], request.form['name'])
			if request.form['email']:
				data += "EMAIL:%s\n" % request.form['email']
			if request.form['mobile']:
				data += "TEL;CELL;PREF:%s\n" % request.form['mobile']
			if request.form['address']:
				data += "ADR;HOME:;;%s;%s;%s;%s\n" \
				% (request.form['address'], request.form['city'], request.form['cap'], request.form['nation'])
			if request.form['website']:
				data += "URL:%s\n" % request.form['website']
			data += "END:VCARD"
		elif request.form['Wifi Name']:
			data = "WIFI:S:%s;T:%s;P:%s;;" \
				% ( request.form['Wifi Name'],
					request.form['password_type'],
					request.form['password'])
		else:
			data = request.form['qr']

		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=10,
		    border=4)
		qr.add_data(data)
		qr.make(fit=True)

		filename = urllib.quote_plus(data)

		img = qr.make_image(fill_color="black", back_color="transparent")
		img.save(open("src/static/qr/%s.png" % filename,'wb'))
		img = "qr/%s.png" % filename
		return render_template('qr.html', data=data, img=img)
	return render_template('qr.html')
