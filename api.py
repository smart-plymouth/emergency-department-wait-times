import boto3
import json
import datetime

from flask import Flask
from flask import jsonify


app = Flask(__name__)
BUCKET = "aggregator-nhs-ed-wait-times-data"


def get_facility_by_id(facility_id):
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, 'facilities.json')
    data = json.loads(obj.get()['Body'].read().decode('utf-8'))
    selected_facility = None

    for facility in data.get('facilities'):
        if facility.get('id') == facility_id:
            selected_facility = facility

    return selected_facility


def get_data_by_range(facility_id, start_date, end_date):
    date_diff = end_date - start_date
    days_diff = date_diff.days
    data = []
    for x in range(0, days_diff + 1):
        current_date = start_date + datetime.timedelta(days=x)
        data.extend(get_data_by_date(facility_id, current_date))
    return data


def get_data_by_date(facility_id, date):
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, '%s/%s/%s/%s.json' % (
        facility_id,
        date.year,
        date.month,
        date.day
    ))
    data = json.loads(obj.get()['Body'].read().decode('utf-8'))
    return data


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


@app.route('/facilities/<string:facility_id>')
def get_facility(facility_id):
    facility = get_facility_by_id(facility_id)

    if not facility:
        return 'Not Found', 404

    facility['data'] = []

    # By default get last 24 hours of readings...
    now = datetime.datetime.utcnow()
    start_date = now - datetime.timedelta(hours=24)
    end_date = now
    data = get_data_by_range(facility_id, start_date, end_date)
    facility['data'].append(data)

    return jsonify(facility)
