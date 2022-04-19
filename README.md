# Chainlink MQTT Relay External Adapter Template

![Lint and unit testing](https://github.com/Briojas/CL-EA-MQTT-Client/workflows/Lint%20and%20unit%20testing/badge.svg)

This template shows basic usecases of an external adapter connecting a Smart Contract to an MQTT Broker. It can be ran locally, or in Docker.

## External Adapter Setup
1. Download and unzip the repo.
2. Install dependencies:
  ```
  pipenv install
  ```
3. Build the docker image and run the container:
  ```
  docker build . -t cl-ea-mqtt-client
  docker run -it -p 8080:8080 cl-ea-mqtt-client
  ```
4. Bridge setup
    - Name: cl-ea-mqtt-client
    - URL: http://192.168.?.??:8080
5. Job setup
    - See oracleJobs directory for examples
  
## Baked-in Features
| action | topic | qos | payload | retain |
| publish | address in Broker | quality of service level | data | storage on Broker |
| subscribe | address of data in Broker | quality of service level | ignored | ignored |
| ipfs | ignored | ignored | ipfs hash | ignored |

[HiveMQ: MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)

## Development 
### Test
  ```
  cd tests
  pipenv run pytest
  ```
### Management
  New packages:
  ```
  pipenv install PYPI-package-name
  ```
  Locking packages:
  ```
  pipenv lock -r > requirements.txt
  ```

| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |
| Paragraph | Text |