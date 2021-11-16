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
    error = False

    def __init__(self, input):
        self.id = input.get('id', 'NONE')
        self.request_data = input.get('data')
        
        self.validate_request_data()
        self.id_action()
        self.build_bridges()
        self.measure_consensus()

    def validate_request_data(self):
        if self.request_data is None or self.request_data == {}:
            self.result_error('No data provided')

    def id_action(self):
        if not self.error:
            for action in self.action_list:
                if self.request_data[action] is not None:
                    self.action = action
                    return
            self.result_error('Invalid action provided')

    def build_bridges(self):
        if not self.error:
            for bridge in self.bridges:
                for action in self.action_list:
                    if self.action == action:
                        try:
                            getattr(bridge, action)(*self.request_data)
                        except Exception as e:
                            self.result_error(e)

    def measure_consensus(self):
        consensus = {
            'subscribe': [],
            'publish': 0
        }
        if not self.error:
            for bridge in self.bridges:
                if self.action == 'subscribe':
                    response = self.bridge.request(self.base_url, params)
                    data = response.json()
                if self.action == 'publish':
                    if
            self.result = data[self.to_param]
            data['result'] = self.result
            self.result_success(data)
        
        self.bridges = None

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.error = True
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
