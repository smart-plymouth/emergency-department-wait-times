# Emergency Department Wait Time Aggregator

This service aggregates wait time data from Plymouth University Hospitals NHS Trust and makes the 
time series data available via an API. Wait times are retrieved from https://www.plymouthhospitals.nhs.uk/urgent-waiting-times
by a Lambda function which scrapes the contents of the page, this is triggered every 5 minutes by Event Bridge.
Retrieved data is stored within an S3 bucket and then served by an API also hosted via Lambda and API Gateway.

## API Endpoint
* https://sjwnchdg79.execute-api.eu-west-1.amazonaws.com/

## API Routes
### /facilities
Returns a list of facilities which are monitored.

#### Example Request
```curl 'https://sjwnchdg79.execute-api.eu-west-1.amazonaws.com/facilities' | jq```

#### Example Response
```
{
  "facilities": [
    {
      "address": "Derriford Hospital, Derriford Road, Crownhill, Plymouth, Devon, PL6 8DH",
      "id": "102b6f1d-8898-4910-99f0-c5d2d449f5d3",
      "latitude": -4.1133,
      "longitude": 50.4168,
      "name": "Derriford Hospital Emergency Department",
      "nhs_trust": "University Hospitals Plymouth NHS Trust",
      "telephone": "01752 245012",
      "type": "Emergency Department",
      "url": "https://www.plymouthhospitals.nhs.uk/urgent-waiting-times"
    },
    {
      "address": "Cumberland Centre, Damerell Close, Devonport, Plymouth, Devon, PL1 4JZ",
      "id": "f228431b-2d19-4f83-b318-19180934834c",
      "latitude": -4.16884,
      "longitude": 50.36999,
      "name": "Cumberland Centre",
      "nhs_trust": "University Hospitals Plymouth NHS Trust",
      "telephone": "01752 434400",
      "type": "Urgent Treatment Centre",
      "url": "https://www.plymouthhospitals.nhs.uk/urgent-waiting-times"
    },
    {
      "address": "Tavistock Hospital, Springhill, Tavistock, Devon, PL19 8LD",
      "id": "cc2ba4fc-aab9-414c-bf46-875f838fd567",
      "latitude": -4.15372,
      "longitude": 50.54724,
      "name": "Tavistock Minor Injuries Unit",
      "nhs_trust": "University Hospitals Plymouth NHS Trust",
      "telephone": "01752 434390",
      "type": "Minor Injuries Unit",
      "url": "https://www.plymouthhospitals.nhs.uk/urgent-waiting-times"
    },
    {
      "address": "South Hams Hospital, Plymouth Road, Kingsbridge, Devon, TQ7 1AT",
      "id": "0941bcf6-194f-4ad7-b7b7-9e0d6b18cdd5",
      "latitude": -3.78142,
      "longitude": 50.28938,
      "name": "Kingsbridge Minor Injuries Unit",
      "nhs_trust": "University Hospitals Plymouth NHS Trust",
      "telephone": "01548 852349",
      "type": "Minor Injuries Unit",
      "url": "https://www.plymouthhospitals.nhs.uk/urgent-waiting-times"
    }
  ],
  "last_updated": "2023-07-05T12:01:00Z"
}
```

## API Routes
### /facilities/<facility_id>
Returns the facility meta-data and time series data. Longest wait times are provided in minutes.
Optionally start and end query string args may be sent with the request to request a custom date range of data using ISO formatted dates.

e.g. ?start=2023-07-05&end=2023-07-05

#### Example Request
```curl --location --request GET 'https://sjwnchdg79.execute-api.eu-west-1.amazonaws.com/facilities/f228431b-2d19-4f83-b318-19180934834c' | jq```

#### Example Response
```
{
  "address": "Cumberland Centre, Damerell Close, Devonport, Plymouth, Devon, PL1 4JZ",
  "data": [
    [
      {
        "dt": "2023-7-5T12:25:26Z",
        "longest_wait": 163,
        "patients_in_department": 20,
        "patients_waiting": 19
      },
      {
        "dt": "2023-7-5T12:30:28Z",
        "longest_wait": 142,
        "patients_in_department": 20,
        "patients_waiting": 20
      },
      {
        "dt": "2023-7-5T12:35:28Z",
        "longest_wait": 142,
        "patients_in_department": 20,
        "patients_waiting": 20
      },
      {
        "dt": "2023-7-5T12:40:25Z",
        "longest_wait": 142,
        "patients_in_department": 20,
        "patients_waiting": 20
      },
      {
        "dt": "2023-7-5T12:45:28Z",
        "longest_wait": 142,
        "patients_in_department": 20,
        "patients_waiting": 20
      },
      {
        "dt": "2023-7-5T12:50:26Z",
        "longest_wait": 107,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T12:55:28Z",
        "longest_wait": 112,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T13:0:26Z",
        "longest_wait": 112,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T13:5:31Z",
        "longest_wait": 112,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T13:10:28Z",
        "longest_wait": 128,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:15:29Z",
        "longest_wait": 128,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:20:25Z",
        "longest_wait": 128,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:25:28Z",
        "longest_wait": 134,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:30:26Z",
        "longest_wait": 140,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T13:35:28Z",
        "longest_wait": 144,
        "patients_in_department": 24,
        "patients_waiting": 24
      },
      {
        "dt": "2023-7-5T13:40:28Z",
        "longest_wait": 150,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:45:25Z",
        "longest_wait": 150,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:50:25Z",
        "longest_wait": 148,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T13:55:25Z",
        "longest_wait": 151,
        "patients_in_department": 25,
        "patients_waiting": 25
      },
      {
        "dt": "2023-7-5T14:0:28Z",
        "longest_wait": 160,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:5:25Z",
        "longest_wait": 164,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:10:29Z",
        "longest_wait": 169,
        "patients_in_department": 28,
        "patients_waiting": 28
      },
      {
        "dt": "2023-7-5T14:15:25Z",
        "longest_wait": 0,
        "patients_in_department": 0,
        "patients_waiting": 0
      },
      {
        "dt": "2023-7-5T14:20:28Z",
        "longest_wait": 179,
        "patients_in_department": 31,
        "patients_waiting": 31
      },
      {
        "dt": "2023-7-5T14:25:28Z",
        "longest_wait": 156,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:30:28Z",
        "longest_wait": 161,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:35:25Z",
        "longest_wait": 166,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:40:28Z",
        "longest_wait": 156,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:45:28Z",
        "longest_wait": 0,
        "patients_in_department": 0,
        "patients_waiting": 0
      },
      {
        "dt": "2023-7-5T14:50:29Z",
        "longest_wait": 167,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T14:55:28Z",
        "longest_wait": 171,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T15:0:28Z",
        "longest_wait": 167,
        "patients_in_department": 30,
        "patients_waiting": 30
      },
      {
        "dt": "2023-7-5T15:5:28Z",
        "longest_wait": 167,
        "patients_in_department": 30,
        "patients_waiting": 30
      },
      {
        "dt": "2023-7-5T15:10:28Z",
        "longest_wait": 177,
        "patients_in_department": 33,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:15:25Z",
        "longest_wait": 182,
        "patients_in_department": 33,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:20:32Z",
        "longest_wait": 187,
        "patients_in_department": 35,
        "patients_waiting": 35
      },
      {
        "dt": "2023-7-5T15:25:28Z",
        "longest_wait": 192,
        "patients_in_department": 35,
        "patients_waiting": 35
      },
      {
        "dt": "2023-7-5T15:30:26Z",
        "longest_wait": 194,
        "patients_in_department": 34,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:35:28Z",
        "longest_wait": 200,
        "patients_in_department": 34,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:40:25Z",
        "longest_wait": 204,
        "patients_in_department": 34,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:45:28Z",
        "longest_wait": 209,
        "patients_in_department": 34,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:50:28Z",
        "longest_wait": 196,
        "patients_in_department": 35,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T15:55:28Z",
        "longest_wait": 201,
        "patients_in_department": 35,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T16:0:25Z",
        "longest_wait": 207,
        "patients_in_department": 34,
        "patients_waiting": 32
      },
      {
        "dt": "2023-7-5T16:5:28Z",
        "longest_wait": 211,
        "patients_in_department": 33,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T16:10:28Z",
        "longest_wait": 216,
        "patients_in_department": 33,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T16:15:25Z",
        "longest_wait": 221,
        "patients_in_department": 33,
        "patients_waiting": 33
      },
      {
        "dt": "2023-7-5T16:20:25Z",
        "longest_wait": 227,
        "patients_in_department": 30,
        "patients_waiting": 30
      },
      {
        "dt": "2023-7-5T16:25:28Z",
        "longest_wait": 231,
        "patients_in_department": 30,
        "patients_waiting": 30
      },
      {
        "dt": "2023-7-5T16:30:29Z",
        "longest_wait": 236,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T16:35:25Z",
        "longest_wait": 241,
        "patients_in_department": 27,
        "patients_waiting": 27
      },
      {
        "dt": "2023-7-5T16:40:25Z",
        "longest_wait": 207,
        "patients_in_department": 26,
        "patients_waiting": 26
      },
      {
        "dt": "2023-7-5T16:45:26Z",
        "longest_wait": 186,
        "patients_in_department": 26,
        "patients_waiting": 26
      },
      {
        "dt": "2023-7-5T16:50:28Z",
        "longest_wait": 191,
        "patients_in_department": 26,
        "patients_waiting": 26
      },
      {
        "dt": "2023-7-5T16:55:25Z",
        "longest_wait": 196,
        "patients_in_department": 26,
        "patients_waiting": 26
      },
      {
        "dt": "2023-7-5T17:0:25Z",
        "longest_wait": 201,
        "patients_in_department": 22,
        "patients_waiting": 22
      },
      {
        "dt": "2023-7-5T17:5:25Z",
        "longest_wait": 206,
        "patients_in_department": 22,
        "patients_waiting": 22
      },
      {
        "dt": "2023-7-5T17:10:33Z",
        "longest_wait": 211,
        "patients_in_department": 22,
        "patients_waiting": 22
      },
      {
        "dt": "2023-7-5T17:15:25Z",
        "longest_wait": 216,
        "patients_in_department": 22,
        "patients_waiting": 22
      }
    ]
  ],
  "id": "f228431b-2d19-4f83-b318-19180934834c",
  "latitude": -4.16884,
  "longitude": 50.36999,
  "name": "Cumberland Centre",
  "nhs_trust": "University Hospitals Plymouth NHS Trust",
  "telephone": "01752 434400",
  "type": "Urgent Treatment Centre",
  "url": "https://www.plymouthhospitals.nhs.uk/urgent-waiting-times"
}
```

