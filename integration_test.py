import adapter

job_run_id = '1'
topics = [
    '/cl-ea-mqtt-client/test1',
    '/cl-ea-mqtt-client/test2',
    '/cl-ea-mqtt-client/test3',
]
test_data = {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': 'testMessage', 'retain': True}
    ]}}

a = adapter.Adapter(test_data)

print(a.result)

test_data = {'id': job_run_id, 'data': {'subscribe': {'topics': [topics[0]], 'qos': 0}}}

b = adapter.Adapter(test_data)

#print(b.result)
