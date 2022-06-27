import json
from flask import jsonify, request
from utils.db import db, Chistes, ChistesSchema
import requests
import random
from math import lcm, gcd

#   Extraccion api chistes chuck y dad
def generador_chiste():
    chuck = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
    dad = requests.get(
        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
    ).json()["joke"]
    random_ = {'Dad':dad, 'Chuck':chuck}
    ra = random.choice(list(random_.keys()))
    dict = {'Dad': dad, 'Chuck': chuck, ',': random_[ra], 'tipo': ra}
    return dict 

#   Programa method GET  
def index(tipo):
    dict = generador_chiste()
    try:
        resultado = dict[tipo]
        return jsonify(resultado)
    except:
        return jsonify('Valor incorrecto.')

#   Programa method POST
def post(tipo):
    try:
        dict = generador_chiste()
        if tipo == ',':
            resultado = dict[tipo]
            nuevo_chiste = Chistes(resultado, dict['tipo'])
        else:
            resultado = dict[tipo]
            nuevo_chiste = Chistes(resultado, tipo)
        db.session.add(nuevo_chiste)
        db.session.commit()
        return jsonify(resultado)
    except:
        return jsonify('Valor incorrecto.')
    
#   Programa method PUT
def update(id, text):
    update_chiste = Chistes.query.get_or_404(int(id))
    try:
        update_chiste.chiste = text
        db.session.commit()
    except Exception as e:
        return jsonify({'Error': 'Invalid request, try again.'})    
    return jsonify({'Success': 'El chiste fue actualizado'})

#   Programa method DELETE
def delete(id):
    chiste = Chistes.query.get_or_404(int(id))
    db.session.delete(chiste)
    db.session.commit()
    return jsonify({'Success': 'El chiste fue eliminado'})    
    
#   Programa DB visualizar
def get_all():
    chiste = Chistes.query.all()
    chistes = [[i.id, i.chiste, i.tipo_chiste] for i in chiste]
    print(chistes)
    print(type(chiste))
    return jsonify(chistes)

#   Programa MCM
def minimo_comun_multiplo():
    lista = request.args.get('lista_numeros').split(',')
    lista = tuple(list(map(int, lista)))
    lcm = 1
    for i in lista:
        lcm = lcm*i//gcd(lcm, i)
    return jsonify(lcm)

#   Programa SUMAR
def suma(numero):
    return jsonify(int(numero) + 1) 