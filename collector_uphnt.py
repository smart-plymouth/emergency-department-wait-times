import logging
import requests
import datetime
import boto3
import json

from bs4 import BeautifulSoup


logging.basicConfig(encoding='utf-8', level=logging.INFO)
BUCKET = "aggregator-nhs-ed-wait-times-data"


def write_data(facility_id, data):
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
        facility_id,
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
    return raw


def main(ctx, evt):
    try:
        logging.info("Extracting UHPNT Urgent Wait Times")
        content = fetch_data()
        raw = extract_data(content)

        # Handle Derriford Data
        try:
            facility_id = "102b6f1d-8898-4910-99f0-c5d2d449f5d3"
            data = {
                'longest_wait': int(raw[0].text),
                'patients_waiting': int(raw[1].text),
                'patients_in_department': int(raw[2].text)
            }
            logging.info("Derriford Data: %s" % data)
            write_data(facility_id, data)
        except Exception as err:
            logging.error("Error processing Derriford data: %s" % str(err))

        # Handle Cumberland Centre Data
        try:
            facility_id = "f228431b-2d19-4f83-b318-19180934834c"
            data = {
                'longest_wait': int(raw[3].text),
                'patients_waiting': int(raw[4].text),
                'patients_in_department': int(raw[5].text)
            }
            logging.info("Cumberland Centre Data: %s" % data)
            write_data(facility_id, data)
        except Exception as err:
            logging.error("Error processing Cumberland Centre data: %s" % str(err))

        # Handle Tavistock Minor Injuries Data
        try:
            facility_id = "cc2ba4fc-aab9-414c-bf46-875f838fd567"
            data = {
                'longest_wait': int(raw[6].text),
                'patients_waiting': int(raw[7].text),
                'patients_in_department': int(raw[8].text)
            }
            logging.info("Tavistock MIU Data: %s" % data)
            write_data(facility_id, data)
        except Exception as err:
            logging.error("Error processing Tavistock MIU data: %s" % str(err))

        # Handle Kingsbridge Minor Injuries Data
        try:
            facility_id = "0941bcf6-194f-4ad7-b7b7-9e0d6b18cdd5"
            data = {
                'longest_wait': int(raw[9].text),
                'patients_waiting': int(raw[10].text),
                'patients_in_department': int(raw[11].text)
            }
            logging.info("Kingsbridge MIU Data: %s" % data)
            write_data(facility_id, data)
        except Exception as err:
            logging.error("Error processing Kingsbridge MIU data: %s" % str(err))

        logging.info("Complete")
    except Exception as e:
        logging.error("Error occured: %s" % str(e))


if __name__ == '__main__':
    main({}, {})
