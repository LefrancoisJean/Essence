# coding:utf-8

import xmltodict
import zipfile
import requests
import json

from io import BytesIO
from flask import Flask, render_template, request, Response, json, g

app = Flask(__name__)

def download_zip():
    print('Téléchargement des données')
    zip_url = 'https://donnees.roulez-eco.fr/opendata/instantane'
    file = requests.get(zip_url)
    with zipfile.ZipFile(BytesIO(file.content)) as zip_file:
        for myzip in zip_file.namelist():
            with zip_file.open(myzip) as myfile:
                liste_station = myfile.read()

    return xmltodict.parse(liste_station, process_namespaces=False)


def trouve_station(liste_station, code_postal):
    liste = {}

    for pdv_liste in liste_station.values():
        for pdvs in pdv_liste.values():
            for i, v in enumerate(pdvs):
                if v['ville']:
                    if v['@cp']==code_postal or v['ville'].lower()==code_postal.lower():
                        liste[i] = v
                else:
                    if v['@cp']==code_postal:
                        liste[i] = v
    with open('test.txt', 'w') as f:
        f.write(json.dumps(liste, indent=2))
    return liste


def run(liste_station, code_postal):
    result = trouve_station(liste_station, code_postal)
    return result

liste_station = download_zip()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def calcul():
    code_postal = request.form['code_postal']
    result = run(liste_station, code_postal)
    return render_template("liste_station.html", code_postal=code_postal, result=result)

