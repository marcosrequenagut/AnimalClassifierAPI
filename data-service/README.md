# Data service for the py_challenge
This project contains a small REST API that will provide the data required to implement the rest of the challenge.

This README is intentionally light on details on how to use the API or the data that is provided, but there should be enough information to complete the challenge by running the API and reading the documentation of the endpoints. Go look for it!

## Features

- Animal classification using a pre-trained Random Forest model
- REST API built with FastAPI
- Interactive dashboard with Streamlit
- Data persistence in SQL database
- Model retraining capability

## Instalation

Clone the repository:
```bash
$ git clone https://github.com/marcosrequenagut/animal-classification-api
```

### How to run in Docker?

To build the image run:
```bash
$ docker build -t py_challenge_data_service:latest .
```
### How to run the API of FastApi?
Then to run the API use:
```bash
$ python -m uvicorn py_challenge_data_service.app:app --reload --host 127.0.0.1 --port 8777
```
You can then start using it from http://127.0.0.1:8777

### How to run the Streamlit Dashboard?
Note: The FastAPI app must be running before starting the Streamlit dashboard. Streamlit interacts with the FastAPI app, so ensure that the API is up and running first.

Once the API is running, you can start the Streamlit dashboard with the following command:
```bash
$ streamlit run data-service/src/py_challenge_data_service/dashboard.py 
```


### How to test its working?
You can send a request through [curl](https://curl.se/)
```bash
$ curl -X 'POST' \
  'http://localhost:8777/api/v1/animals/data' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "seed": 42,
  "number_of_datapoints": 500
}'
```
