import time
import os

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import calendar_api
import period

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/upload', methods = ['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "period.csv"))
    else:
        return {'resultStatus': 'FAILURE'}
    return {'resultStatus': 'SUCCESS'}

@app.route('/api/period', methods = ['GET'])
def get_period():
    period_file = os.path.join(UPLOAD_FOLDER, "period.csv")
    return period.read_period_file(period_file)

@app.route('/api/suggestions', methods = ['GET'])
def get_suggestions():
    period_file = os.path.join(UPLOAD_FOLDER,"period.csv")
    return period.suggestion_pipeline(period_file)