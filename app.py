# coding:utf-8
from flask import Flask, render_template, request
import essence

app = Flask(__name__)

liste_station = essence.download_zip()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def calcul():
    code_postal = request.form['code_postal']
    result = essence.run(liste_station, code_postal)
    return render_template("liste_station.html", code_postal=code_postal, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

