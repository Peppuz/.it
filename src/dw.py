from src import app
from flask import redirect, send_from_directory, jsonify

@app.route('/dw/<file_name>', methods=['GET'])
def dw(file_name):
	return send_from_directory('dw', filename=file_name, as_attachment=True)
