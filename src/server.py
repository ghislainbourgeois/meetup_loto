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
        if _parameters_valid(meetup_name, event_id):
            _setup_session(meetup_name, event_id)
            return redirect(url_for('details'))
        else:
            error = "Invalid characters"
            return render_template('index.html', error=error)

@app.route('/details')
def details():
    loto = _get_loto()
    return render_template('details.html', participants=loto.number_of_participants(), chances=loto.current_chances())

@app.route('/draw')
def draw():
    loto = _get_loto()
    winner = dict()
    winner['id'] = loto.draw()
    if winner['id'] != 0:
        winner['name'] = loto.get_member_name(winner['id'])
        winner['photo'] = loto.get_member_photo_url(winner['id'])
        return render_template('draw.html', winner=winner)
    else:
        return render_template('draw.html', error="Sorry, there are no more participants to draw from")

def _get_loto():
    return cache[session['id']]['loto']

def _parameters_valid(meetup_name, event_id):
    return re.fullmatch('[0-9a-zA-Z-]*', meetup_name) and re.fullmatch('[0-9]*', event_id)

def _setup_session(meetup_name, event_id):
            session['id'] = os.urandom(8)
            cache[session['id']] = dict()
            cache[session['id']]['meetup_name'] = meetup_name
            cache[session['id']]['event_id'] = event_id
            cache[session['id']]['loto'] = Loto(app.config['api'], meetup_name, event_id)

app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT"))
