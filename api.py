import boto3
import json

from flask import Flask
from flask import jsonify


app = Flask(__name__)
BUCKET = "aggregator-nhs-ed-wait-times-data"


@app.route("/")
def get_app_version():
    app_data = {
        "service": "NHS Emergency Department Wait Times Aggregator API",
        "version": 1.0
    }
    return jsonify(app_data)


@app.route('/facilities')
def get_facilities():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, 'facilities.json')
    return jsonify(json.loads(obj.get()['Body'].read().decode('utf-8')))
