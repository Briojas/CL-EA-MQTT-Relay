from bridge import Bridge


class Adapter:
    bridges = [
        Bridge(
            'mqtt.eclipse.org', 
            1883
        ),
        Bridge(
            'test.mosquitto.org', 
            1883
        ),
        Bridge(
            'broker.hivemq.com', 
            1883
        )
    ]

    action_list = ['subscribe', 'publish']
    action = ''
    final_message = {}

    def __init__(self, input):
        self.id = input.get('id', 'NONE')
        self.request_data = input.get('data')
        if self.validate_request_data():
            if self.id_action():
                self.build_bridges()
                self.measure_consensus()
                self.bridges = None
            else:
                self.result_error('Invalid action provided')
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def id_action(self):
        for action in self.action_list:
            if self.request_data[action] is not None:
                self.action = action
                return True
        return False

    def build_bridges(self):
        for bridge in self.bridges:
            for action in self.action_list:
                if self.action == action:
                    try:
                        getattr(bridge, action)(*self.request_data)
                    except Exception as e:
                        self.result_error(e)

    def measure_consensus(self):
        params = {
            'fsym': self.from_param,
            'tsyms': self.to_param,
        }
        response = self.bridge.request(self.base_url, params)
        data = response.json()
        self.result = data[self.to_param]
        data['result'] = self.result
        self.result_success(data)

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
