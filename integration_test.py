import adapter
from time import sleep

job_run_id = '1'
topics = [
    '/cl-ea-mqtt-client/test1',
    '/cl-ea-mqtt-client/test2',
    '/cl-ea-mqtt-client/test3',
]
test_data = {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': 'testMessage', 'retain': True}
    ]}}
test_data = {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': 5, 'retain': True}
    ]}}
print('starting a')
a = adapter.Adapter(test_data)
print(a.result)

print('starting b')
test_data = {'id': job_run_id, 'data': {'subscribe': {'topics': [topics[0]], 'qos': 0}}}

b = adapter.Adapter(test_data)
print(b.result)
b = None