import boto3
import json
import datetime
import dateutil

from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS


app = Flask(__name__)
CORS(app)
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
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(BUCKET, '%s/%s/%s/%s.json' % (
            facility_id,
            date.year,
            date.month,
            date.day
        ))
        data = json.loads(obj.get()['Body'].read().decode('utf-8'))
        return data
    except Exception:
        return []


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
        return jsonify(
            {
                'error': 'Not Found',
                'status': 404,
                'message': 'Facility not found.'
            }
        ), 400

    facility['data'] = []

    now = datetime.datetime.utcnow()

    start = request.args.get('start')
    if start:
        start_dt = dateutil.parser.parse(start)
    else:
        start_dt = now - datetime.timedelta(hours=24)

    end = request.args.get('end')
    if end:
        end_dt = dateutil.parser.parse(end)
    else:
        end_dt = now

    if end_dt < start_dt:
        return jsonify(
            {
                'error': 'Bad Request',
                'status': 400,
                'message': 'End date must be after start date.'
            }
        ), 400

    data = get_data_by_range(facility_id, start_dt, end_dt)
    facility['data'].extend(data)

    return jsonify(facility)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=False)
