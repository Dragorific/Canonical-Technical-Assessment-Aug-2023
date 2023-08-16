from flask import Flask, render_template
from database import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    events = query_events({})
    return render_template('events.html', events=events)

def start_flask_app():
    app.run()
