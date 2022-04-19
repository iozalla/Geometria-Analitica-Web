from ast import Global

import flask

import re

from datetime import datetime, timedelta
from json import dumps, load, loads

from flask import Flask, redirect, session, render_template, request, flash, url_for,make_response
import database

global foroActual
foroActual = -1

app = Flask(__name__)
app.secret_key = '*nW6Ze{|=p-Whj3FA%V+0xGwC~\OXY^6B=979NO2'


@app.route('/pdf')
def pdfviewer():
    number=int(request.args.get('id'))
    print(number)
    if number ==1:
        return redirect("/static/docs/1_Iniciación.pdf")
    elif number==2:
        return redirect("/static/docs/2_Vectores.pdf")
    elif number==3:
        return redirect("/static/docs/3_OperacionesV.pdf")
    elif number==4:
        return redirect("/static/docs/4_EcuacionesR.pdf")
    elif number==5:
        return redirect("/static/docs/5_ProblemasI.pdf")
    elif number==6:
        return redirect("/static/docs/Todos.pdf")
    else:
        return 

@app.route('/', methods=['GET'])
def index():
    return render_template('temas.html')

@app.route('/main/', methods=['GET'])
def main():
    """Return the index.html page"""
    return render_template('index.html')
@app.route('/teoria/', methods=['GET'])
def teoria():
    """Return the teoria.html page"""
    return render_template('teoria.html')


@app.route('/ejercicios/', methods=['GET'])
def ejercicios():
    """Return the ejercicios.html page"""
    tests = database.get_tests()
    return render_template('ejercicios.html', tests=tests)


@app.route('/correccion_ejercicios/', methods=['POST'])
def correccion():
    tests = database.get_tests()
    correccion = []
    for id, question, a, b, c, d, answer in tests:
        try:
            respondido = request.form[str(id)]
        except:
            respondido = None
        correccion.append((id, question, {'a':a, 'b':b, 'c':c, 'd':d}, answer, respondido))
            
    return render_template('correccion_ejercicios.html', correciones=correccion)

@app.route('/foro/', methods=['GET','POST'])
def foro():
    try:
        session['email']
    except:
        return redirect(url_for("login"), code=302)
    if not(session['email'] is None):
        id=request.args.get('id')
        if not(id is None):
            print("ACTUALIZAR GLOBAL: "+id,foroActual)
            tests = database.get_hilo(id)
            globals()["foroActual"]=id
            return render_template('foro.html', tests=tests)
        else:
            tests = database.get_hilos()
            print(tests)
            return render_template('foroMain.html', tests=tests)
    else:
        return redirect(url_for("login"), code=302)

@app.route('/crearHilo/', methods=['GET','POST'])
def crearHilo():
    try:
        session['email']
    except:
        return redirect(url_for("login"), code=302)
    if not(session['email'] is None):
        if flask.request.method == 'POST':
            try:
                text=request.form['text']
                database.crear_post(text,session['email'],-1)
                return redirect(url_for('foro'))
            except:
                text=request.form['text2']
                database.crear_post(text,session['email'],foroActual)
                return redirect(url_for('foro')+"?id="+foroActual)
        else:
            return render_template('crearHilo.html')
    else:
        return redirect(url_for("login"), code=302)
    
@app.route('/login/', methods=['GET','POST'])
def login():
    if flask.request.method == 'POST' :
        if (user_data := database.get_user_data(request.form['email'])) != None and request.form['password'] == user_data[2]:
            session['email'] = request.form['email']
            session['nombre'] = user_data[0].title()
            session['apellido'] = user_data[1].title()
            return render_template('index.html')
        else:
            flash('Email o contraseña incorrectos.')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/signup/', methods=['GET','POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        database.register_user(request.form['email'],request.form['name'].title(),request.form['last_name'].title(),request.form['password'], request.form['rol'])
        session['email'] = request.form['email']
        session['nombre'] = request.form['name'].title()
        session['apellido'] = request.form['last_name'].title()
        return render_template('index.html')


@app.route('/close_session/',methods=['GET'])
def close_session():
    session['email'] = None
    session['nombre'] = None
    session['apellido'] = None
    flash('Sesión cerrada.')
    return render_template('index.html')

def flush_warnings():
    session['_flashes'].clear()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001, debug=True)
