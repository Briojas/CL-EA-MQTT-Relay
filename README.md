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
      - for local deployments
5. Job setup
    - See oracleJobs directory for examples
  
## Baked-in Actions
### Publish
Posts a singular payload to the Brokers defined on the topic specified with the quality of service level given. 
### Subscribe
Gets a singular payload from the Brokers defined on the topic specified with the quality of service level given
### Script
Pulls a script from IPFS at the hash given for advanced, custom processing
#### Inputs table:
| action | topic | qos | payload | retain |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **PUBLISH**[^1] | address in Broker | quality of service level | data | storage on Broker |
| **SUBSCRIBE**[^1] | address in Broker | quality of service level | ignored | ignored |
| **SCRIPT** | ignored | ignored | ipfs hash[^2] | ignored |

[^1]: [HiveMQ: MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
[^2]: [IPFS URL with hash](https://docs.ipfs.io/how-to/address-ipfs-on-web/)

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