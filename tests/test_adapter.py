from numbers import Number
import pytest
import adapter

job_run_id = '1'
topics = [
    '/cl-ea-mqtt-client/test1',
    '/cl-ea-mqtt-client/test2',
    '/cl-ea-mqtt-client/test3',
]
payload_string = 'test_message'
payload_float = 11.11
payload_int = 7

def adapter_setup(test_data):
    a = adapter.Adapter(test_data)
    return a.result

#pub/sub string data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': payload_string, 'retain': True},
        {'topic': topics[1], 'qos': 0, 'payload': payload_string, 'retain': True},
        {'topic': topics[2], 'qos': 0, 'payload': payload_string, 'retain': True}
    ]}},
    {'id': job_run_id, 'data': {'subscribe':{'topics': topics, 'qos':0}}},
])
def test_pub_sub_strings(test_data):
    result = adapter_setup(test_data)
    print(result)
    
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is str
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict

#pub/sub float data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': payload_float, 'retain': True},
        {'topic': topics[1], 'qos': 0, 'payload': payload_float, 'retain': True},
        {'topic': topics[2], 'qos': 0, 'payload': payload_float, 'retain': True}
    ]}},
    {'id': job_run_id, 'data': {'subscribe':{'topics': topics, 'qos':0}}},
])
def test_pub_sub_floats(test_data):
    result = adapter_setup(test_data)
    print(result)
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is float
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict

#pub/sub int data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {'publish': [
        {'topic': topics[0], 'qos': 0, 'payload': payload_int, 'retain': True},
        {'topic': topics[1], 'qos': 0, 'payload': payload_int, 'retain': True},
        {'topic': topics[2], 'qos': 0, 'payload': payload_int, 'retain': True}
    ]}},
    {'id': job_run_id, 'data': {'subscribe':{'topics': topics, 'qos':0}}},
])
def test_pub_sub_ints(test_data):
    result = adapter_setup(test_data)
    print(result)
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is int
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict


@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {}},
    {'id': job_run_id, 'data': {'unknown_action': [{'fake_data': 'does_not_exist'}]}},
    {},
])
def test_error_catching(test_data):
    result = adapter_setup(test_data)
    print(result)
    assert result['statusCode'] == 500
    assert result['jobRunID'] == job_run_id
    assert result['status'] == 'errored'
    assert result['error'] is not None
