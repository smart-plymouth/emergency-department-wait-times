import logging
import requests
import datetime
import boto3
import json

from bs4 import BeautifulSoup


logging.basicConfig(encoding='utf-8', level=logging.INFO)
FACILITY_ID = "102b6f1d-8898-4910-99f0-c5d2d449f5d3"
BUCKET = "aggregator-nhs-ed-wait-times-data"


def write_data(data):
    now = datetime.datetime.utcnow()
    data['dt'] = '%s-%s-%sT%s:%s:%sZ' % (
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )

    file = '%s/%s/%s/%s.json' % (
        FACILITY_ID,
        now.year,
        now.month,
        now.day
    )

    client = boto3.client('s3')
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(BUCKET, file)
        content = obj.get()['Body'].read().decode('utf-8')
        todays_data = json.loads(content)
        todays_data.append(data)
        obj.put(Body=json.dumps(todays_data))
    except Exception as exc:
        logging.error('%s' % str(exc))
        todays_data = []
        todays_data.append(data)
        client.put_object(
            Body=json.dumps(todays_data),
            Bucket=BUCKET,
            Key=file
        )


def fetch_data(
        url='https://www.plymouthhospitals.nhs.uk/urgent-waiting-times'
):
    logging.info("Fetching data from UHPNT website")
    response = requests.get(url, verify=False)
    return response.text


def extract_data(content):
    logging.info("Extracting wait time data")
    soup = BeautifulSoup(content, "html.parser")
    raw = soup.find_all("span", {"class": "data-number"})
    return {
        'longest_wait': int(raw[0].text),
        'patients_waiting': int(raw[1].text),
        'patients_in_department': int(raw[2].text)
    }


def main(ctx, evt):
    try:
        logging.info("Extracting UHPNT Urgent Wait Times")
        content = fetch_data()
        data = extract_data(content)
        logging.info("Writing data: %s" % data)
        write_data(data)
        logging.info("Complete")
    except Exception as e:
        logging.error("Error occured: %s" % str(e))


if __name__ == '__main__':
    main({}, {})
