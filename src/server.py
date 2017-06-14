import os
import re
from flask import Flask, request, render_template, session, redirect, url_for, g
from meetup_api import MeetupApi
from meetup_loto import Loto

app = Flask(__name__)
app.config.update(dict(api=MeetupApi()))

cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    error = None
    if request.method == 'POST':
        meetup_name = request.form['meetup_name']
        event_id = request.form['event_id']
        if re.fullmatch('[0-9a-zA-Z-]*', meetup_name) and re.fullmatch('[0-9]*', event_id):
            session['id'] = os.urandom(8)
            cache[session['id']] = dict()
            cache[session['id']]['meetup_name'] = meetup_name
            cache[session['id']]['event_id'] = event_id
            cache[session['id']]['loto'] = Loto(app.config['api'], meetup_name, event_id)
            return redirect(url_for('details'))
        else:
            error = "Invalid characters"
            return render_template('details.html', error=error)

@app.route('/details')
def details():
    loto = cache[session['id']]['loto']
    return render_template('details.html', participants=loto.number_of_participants(), chances=loto.current_chances())

app.secret_key = os.urandom(24)
