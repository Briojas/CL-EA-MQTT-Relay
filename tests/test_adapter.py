import pytest
import adapter

job_run_id = '1'
topics = [
    '/cl-ea-mqtt-client/test1',
    '/cl-ea-mqtt-client/test2',
    '/cl-ea-mqtt-client/test3',
]

def adapter_setup(test_data):
    a = adapter.Adapter(test_data)
    return a.result

@pytest.mark.parametrize('test_data', [
        #publish single
    {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': 'testMessage', 'retain': True}
    ]}},
        #subscribe single
    {'id': job_run_id, 'data': {'subscribe':{'topics':[topics[0]], 'qos':0}}},
        #publish multiple
    {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': 'testMessage', 'retain': True},
        {'topic': topics[1], 'qos': 0, 'payload': 'testMessage', 'retain': True},
        {'topic': topics[2], 'qos': 0, 'payload': 'testMessage', 'retain': True}
    ]}},
        #subscribe multiple
    {'id': job_run_id, 'data': {'subscribe':{'topics': topics, 'qos':0}}},
])
def test_create_request_success(test_data):
    result = adapter_setup(test_data)
    print(result)
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    assert result['data'] is not None
    assert type(result['result']) is float
    assert type(result['data']['result']) is float


@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {}},
    {'id': job_run_id, 'data': {'from': 'does_not_exist', 'to': 'USD'}},
    {},
])
def test_create_request_error(test_data):
    result = adapter_setup(test_data)
    print(result)
    assert result['statusCode'] == 500
    assert result['jobRunID'] == job_run_id
    assert result['status'] == 'errored'
    assert result['error'] is not None
