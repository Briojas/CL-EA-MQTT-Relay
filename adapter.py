import statistics

from attr import validate
from bridge import Bridge

class Adapter:
    bridges = [
        Bridge(
            'cl-ea-mqtt-test.cloud.shiftr.io', 
            1883,
            'cl-ea-mqtt-test',
            'roW522qXIMaMgKc2'
        ),
        # Bridge(
        #     'broker.mqttdashboard.com', 
        #     8000
        # ),
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
        self.request_data = [input.get('data')]
        
        self.validate_request_data()
        self.id_action()
        self.build_bridge()
        self.build_consensus()
        self.burn_bridge()

    def validate_request_data(self):
        if self.request_data is None or self.request_data == {}:
            self.result_error('No data provided')

    def id_action(self):
        if not self.error:
            for action in self.action_list:
                if action in self.request_data[0]:
                    self.action = action
                    return
            self.result_error('Invalid action provided')

    def build_bridge(self):
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
        if not self.error:
            for bridge in self.bridges:
                responses.append(bridge.result)
                for topic in bridge.messages:
                    create_measure = True
                    for measure in consensus:
                        if measure['topic'] == topic['topic']:
                            measure['payload'].append(topic['payload'])
                            create_measure = False
                            break
                    if create_measure:
                        consensus.append(
                            {
                                'topic': topic['topic'],
                                'payload': [topic['payload']]
                            }
                        )
            self.result = self.measure_consensus(responses)
            for measure in consensus:
                measure['payload'] = self.measure_consensus(measure['payload'])
            self.result_success(consensus)

    def measure_consensus(self, values):
        str_type = False
        for item in values:
            if type(item) is str:
                str_type = True
            elif item is None:
                values.pop(values.index(item))
        if str_type:
            strings = [
                {
                    'value': values[0],
                    'count': 0 #about to count it
                }
            ]
            for item in values:
                for value in strings:
                    if value['value'] == item:
                        value['count'] = value['count'] + 1
                        break
            count = 0
            for value in strings:
                if value['count'] > count:
                    string = value['value']
                    count = value['count']
            measurement = {
                'value': string,
                'agreed': count/len(values),
                'reporting': len(values)/len(self.bridges)
            }
        else:
            measurement = {
                'value': statistics.mean(values),
                'stdev': statistics.stdev(values),
                'variance': statistics.variance(values),
                'reporting': len(values)/len(self.bridges)
            }
        return measurement

    def burn_bridge(self):
        for bridge in self.bridges:
            bridge.disconnect()

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
            'error': error,
            'statusCode': 500,
        }
