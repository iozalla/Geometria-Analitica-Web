from cgi import test
<<<<<<< HEAD
from crypt import methods
import flask
=======
# from crypt import methods
>>>>>>> 53653b4b399811bbc4e29ab6bda72475c3c474c8
import requests
import re

from datetime import datetime, timedelta
from json import dumps, load, loads

from flask import Flask, render_template, Response, request, redirect,url_for

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

@app.route('/login/', methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

@app.route('/signup/', methods=['GET','POST'])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')


        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001, debug=True)
