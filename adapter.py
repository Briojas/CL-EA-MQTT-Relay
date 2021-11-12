from bridge import Bridge


class Adapter:
    brokers = [{
        'Host': 'mqtt.eclipse.org',
        'Port': 1883,
        'User': eclipseUserName,
        'API': ECLIPSE_API_KEY
    },{
        'Host': 'test.mosquitto.org',
        'Port': 1883,
        'User': eclipseUserName,
        'API': ECLIPSE_API_KEY
    },{
        'Host': 'broker.hivemq.com',
        'Port': 1883,
        'User': eclipseUserName,
        'API': ECLIPSE_API_KEY
    }]
    action_list = ['subscribe', 'publish']
    action = ''
    subs_def = {
        'topics': [], 
        'qos': 0
    }
    pub_msg_def = {
        'topic': '',
        'qos': 0, 
        'payload': '', 
        'retain': True
    }

    def __init__(self, input):
        self.id = input.get('id', 'NONE')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.id_action()
            self.create_request()
            self.bridge = Bridge()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def id_action(self):
        for action in self.actions:
            if self.request_data[action] is not None:
                self.action = action
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
