from bridge import Bridge
import statistics
import os
from dotenv import load_dotenv

class Adapter:
    load_dotenv()
    public_broker_hivemq = str(os.environ['PUBLIC_BROKER_HIVEMQ'])
    private_broker_hivemq = str(os.environ['PRIVATE_BROKER_HIVEMQ'])
    hivemq_client_user = str(os.environ['HIVEMQ_CLIENT_USER'])
    hivemq_client_key = str(os.environ['HIVEMQ_CLIENT_KEY'])
    bridges = [
        Bridge(
            'broker.emqx.io', 
            1883,
        ),
        Bridge(
            public_broker_hivemq, #'broker.hivemq.com'
            1883
        ),
        Bridge(
            private_broker_hivemq, 
            8883,
            hivemq_client_user,
            hivemq_client_key
        )
    ]
    action_list = ['subscribe', 'publish']
    action = ''
    error = False

    def __init__(self, input):
        self.id = input.get('id', 1)
        self.request_data = [input.get('data')] #needs to be list for getattr()(*inputs)
        
        self.validate_request_data()
        self.id_action()
        self.build_bridge()
        self.build_consensus()
        self.burn_bridge()

    def validate_request_data(self):
        if self.request_data[0] is None or self.request_data[0] == {}:
            self.result_error('No data provided')

    def id_action(self):
        if not self.error:
            if 'action' in self.request_data[0].keys() and self.request_data[0]['action'] in self.action_list:
                self.action = self.request_data[0]['action']
                return
            self.result_error('Invalid action provided')

    def build_bridge(self):
        if not self.error:
            for bridge in self.bridges:
                try:
                    getattr(bridge, self.action)(*self.request_data)
                except Exception as e:
                    self.result_error(e)

    def build_consensus(self):
        consensus = []
        responses = []
        if not self.error:
            for bridge in self.bridges:
                responses.append(bridge.result)
                print(bridge.messages)
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
        none_items = []
        for item in values:
            if type(item) is str:
                str_type = True
            elif item is None:
                none_items.append(values.index(item))
        none_items.reverse()
        for item in none_items:
            values.pop(item)
        if len(values) == 0:
            measurement = {
                'reporting': 0
            }
        elif str_type:
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
                'value': str(string),
                'agreed': count/len(values),
                'reporting': len(values)/len(self.bridges)
            }
        else:
            if len(values) == 1:
                value = values[0]
                stdev = 0
                variance = 0
            else:
                mode = statistics.mode(values)
                median = statistics.median(values)
                if median == mode:
                    value = mode
                else:
                    value = median
                stdev = statistics.stdev(values)
                variance = statistics.variance(values)
            measurement = {
                'value': value,
                'stdev': stdev,
                'variance': variance,
                'reporting': len(values)/len(self.bridges)
            }
        return measurement

    def burn_bridge(self):
        if not self.error:
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
