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
    error = False

    def __init__(self, input):
        self.id = input.get('id', 'NONE')
        self.request_data = input.get('data')
        
        self.validate_request_data()
        self.id_action()
        self.build_bridges()
        self.build_consensus()

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

    def build_consensus(self):
        consensus = []
        responses = []
        data = []
        if not self.error:
            for bridge in self.bridges:
                responses.append(bridge.result)
                for topic in bridge.messages:
                    create_measure = True
                    for measure in consensus:
                        if measure['topic'] == topic['topic']:
                            measure['payloads'].append(topic['payload'])
                            create_measure = False
                            break
                    if create_measure:
                        consensus.append(
                            {
                                'topic': topic['topic'],
                                'payload': []
                            }
                        )
            
            self.result = self.measure_consensus(responses)
            for measure in consensus:
                data.append(self.measure_consensus(measure['payload']))
            self.result_success(data)
        
        self.bridges = None #clearing bridge connections

    def measure_consensus(self, list):
        measurement = {
            'value': None,
            'num': None,
            'stdDev': None
        }
        for item in list:


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
