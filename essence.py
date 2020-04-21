# coding:utf-8
from io import BytesIO
import xmltodict
import zipfile
import requests


def download_zip():
    liste_station = None
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
            for indice, ville in enumerate(pdvs):
                if ville['ville']:
                    if ville['ville'].replace("-", " ").lower()==code_postal.lower():
                        liste[indice] = ville
                    elif ville['@cp']==code_postal:
                        liste[indice] = ville
                    elif ville['ville'].replace("-", " ").lower().startswith(code_postal):
                        liste[indice] = ville
                    elif ville['@cp'].startswith(code_postal):
                        liste[indice] = ville
                else:
                    if ville['@cp']==code_postal:
                        liste[indice] = ville
    return liste


def run(liste_station, code_postal):
    result = trouve_station(liste_station, code_postal)
    return result
