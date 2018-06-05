from src import app, db, bot
from flask import redirect, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests, json, os, ftplib

""" Extensione Backend Fondo Danilo Dolci """

@app.route("/api/GET/<table>/<token>", methods=['GET'])
def get_table(table, token):
    """
        * Checks if posted data is correct
    """
    if token == 'password':
        with db.cursor() as cursor:
                # Create a new record
                sql = "SELECT * FROM `%s`;"
                try:
                    cursor.execute(sql, (table))
                except Exception as e:
                    return jsonify({"http_code":500, "error":"DB %s" % e})

                return jsonify(cursor.fetchall())
    else:
        return render_template('index.html')
