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