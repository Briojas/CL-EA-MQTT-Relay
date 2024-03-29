from dotenv import load_dotenv
from bridge import Bridge
import os, json, statistics

class Adapter:
    bridges = []
    bridge_hosts = []
    action_list = [action for action in dir(Bridge) if action.startswith('__') is False]
    action = ''
    error = False

    def __init__(self, input):
        self.id = input.get('id', 1)
        self.request_data = [input.get('data')] #needs to be list for getattr()(*inputs)
        
        self.validate_request_data()
        self.id_action()
        self.build_bridges()
        self.execute_bridges()
        self.build_consensus()
        self.burn_bridge_data()

    def validate_request_data(self):
        if self.request_data[0] is None or self.request_data[0] == {}:
            self.result_error('No data provided')

    def id_action(self):
        if not self.error:
            if 'action' in self.request_data[0].keys() and self.request_data[0]['action'] in self.action_list:
                self.action = self.request_data[0]['action']
                return
            self.result_error('Invalid action provided')

    def build_bridges(self):
        load_dotenv()
        with open(os.getcwd() + '/bridges.json', 'r') as readingFile:
            bridges = json.load(readingFile)
        for bridge in bridges['bridges']:
            if bridge['host'] is not None and bridge['host'] not in self.bridge_hosts:
                if bridge['env']:
                    host = str(os.environ[bridge['host']])    
                    user = str(os.environ[bridge['user']])
                    key = str(os.environ[bridge['key']])
                else:
                    host = bridge['host']
                    user = bridge['user']
                    key = bridge['key']
                self.bridges.append(Bridge(
                    host, 
                    bridge['port'],
                    user,
                    key
                ))
                self.bridge_hosts.append(bridge['host'])

    def execute_bridges(self):
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
                #print(bridge.messages) #Debugging
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

    def burn_bridge_data(self):
        if not self.error:
            for bridge in self.bridges:
                bridge.messages = []
                bridge.result = 'failed'

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