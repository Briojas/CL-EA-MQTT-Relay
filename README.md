# Chainlink External Adapter as an MQTT Relay

![Lint and unit testing](https://github.com/Briojas/CL-EA-MQTT-Client/workflows/Lint%20and%20unit%20testing/badge.svg)

This template shows basic usecases of a Chainlink external adapter connecting a smart contract to an MQTT broker. It can be ran locally or in Docker.

## Setup
1. Download and unzip the repository.
2. Install dependencies:
      ```
      pipenv install
      ```
3. Populate 'bridges.json' file:
    - **'name'**: Label describing this broker bridge
    - **'host'**: Domain name or IP address of the broker
    - **'port'**: Unsecure (e.g. 1883) or secure (e.g. 8883) broker port number
    - **'user'**: Username for logging into private brokers
    - **'key'**: Password for logging into private broker
    - **'env'**: Flags if the 'host', 'user', and 'key' values are .env file variable names
4. Create '.env' file with any private broker data.
    - Be sure the variable names created match those listed in the 'bridges.json' file:
      ```
      JSON File:
      "host": "PRIVATE_BROKER_DOMAIN"

      .env File:
      PRIVATE_BROKER_DOMAIN = some.broker.domain
      ```
5. Build the docker image and run the container:
      ```
      docker build . -t cl-ea-mqtt-client
      docker run -it -p 8080:8080 cl-ea-mqtt-client
      ```
6. Setup the [node bridge](https://docs.chain.link/docs/node-operators/).
7. Create the [node job](https://docs.chain.link/docs/jobs/).
    - See [oracleJobs](https://github.com/Briojas/CL-EA-MQTT-Client/tree/master/oracleJobs) directory for TOML examples utilizing this bridge
8. Submit data/action requests via a [ChainlinkClient compatible hybrid smart contract.
  
## Baked-in Actions
### Publish
Posts a singular payload to the Brokers defined on the topic specified with the quality of service level given. 
### Subscribe
Gets a singular payload from the Brokers defined on the topic specified with the quality of service level given
### Script
Pulls a file from IPFS at the hash given for more advanced and custom processing
#### Inputs table:
| action | topic | qos | payload | retain |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **publish**[^1] | address in Broker | quality of service level | data | store on Broker |
| **subscribe**[^1] | address in Broker | quality of service level | ignored | ignored |
| **script** | ignored | ignored | ipfs hash[^2] | ignored |

[^1]: [HiveMQ: MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
[^2]: [IPFS URL with hash](https://docs.ipfs.io/how-to/address-ipfs-on-web/)

## Development 
### Test
  ```
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