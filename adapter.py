from bridge import Bridge


class Adapter:
    brokers = [{
        “Host”: ‘mqtt.eclipse.org’,
        “Port”: 1883,
        “User”: eclipseUserName,
        “API”: ECLIPSE_API_KEY
    },{
        “Host”: ‘test.mosquitto.org’,
    },{
        “Host”: ‘broker.hivemq.com’]
    }]
    
    actions = [‘subscribe’, ‘publish’]
        #See github.com/eclipse/Paho.mqtt.python for docs
    subscribe_params = ['topic', 'qos']
    publish_params = ['payload', 'retain']

    def __init__(self, input):
        
        self.id = input.get('id', 'NONE')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        for action in self.request_data:
            for param in action:
                
            self.from_param = self.request_data.get(param)
            if self.from_param is not None:
                break
        for param in self.to_params:
            self.to_param = self.request_data.get(param)
            if self.to_param is not None:
                break

    def create_request(self):
        try:
            params = {
                'fsym': self.from_param,
                'tsyms': self.to_param,
            }
            response = self.bridge.request(self.base_url, params)
            data = response.json()
            self.result = data[self.to_param]
            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
