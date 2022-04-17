# Chainlink Python Serverless External Adapter Template

![Lint and unit testing](https://github.com/Briojas/CL-EA-MQTT-Client/workflows/Lint%20and%20unit%20testing/badge.svg)

This template shows a basic usecase of an external adapter written in Python for connecting a Smart Contract to an MQTT Broker. It can be ran locally, in Docker, AWS Lambda, or GCP Functions.

## Install

```
pipenv install
```

## Test

```
pipenv run pytest
```
## Management
For new packages:
```
pipenv install PYPI-package-name
```
Locking new packages:
```
pipenv lock -r > requirements.txt
```
## Run with Docker

Build the image

```
docker build . -t cl-ea-mqtt-client
```

Run the container

```
docker run -it -p 8080:8080 cl-ea-mqtt-client
```