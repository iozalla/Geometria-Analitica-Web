from ast import Try
from cgi import test
from django.shortcuts import render
import flask
import requests
import re

from datetime import datetime, timedelta
from json import dumps, load, loads

from flask import Flask, redirect, session, render_template, request, flash, url_for

import database



def sample_function():
    """This is a sample docstring subject

    This is a sample docstring description.

    Args:
        s (str): a string argument
        i (int): an integer argument

    Returns:
         dict: a dictionary is returned

    Raises:
        Any exception to be caught later.
    """
    return "Hello World"


app = Flask(__name__)
app.secret_key = '*nW6Ze{|=p-Whj3FA%V+0xGwC~\OXY^6B=979NO2'


@app.route('/', methods=['GET'])
def index():
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
            correccion.append((id, question, [a, b, c, d], answer, respondido))
        except:
            print("el usuario no ha respondido a todas las prerguntas")
            #return redirect(url_for('correccion'))
            
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
            id=request.args.get('id')
            tests = database.get_hilo(id)
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
            
            text=request.form['text']
            database.crear_post(text,session['email'])
            return render_template('crearHilo.html')
        else:
            return render_template('crearHilo.html')
    else:
        return redirect(url_for("login"), code=302)
    
@app.route('/login/', methods=['GET','POST'])
def login():
    if flask.request.method == 'POST' and request.form['password'] == (user_data := database.get_user_data(request.form['email']))[2]:
        session['email'] = request.form['email']
        session['nombre'] = user_data[0]
        session['apellido'] = user_data[1]
        print(session['nombre'])
        print(session['apellido'])
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/signup/', methods=['GET','POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        database.register_user(request.form['email'],request.form['name'],request.form['last_name'],request.form['password'], request.form['rol'])
        session['email'] = request.form['email']
        session['nombre'] = request.form['name']
        session['apellido'] = request.form['last_name']
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
