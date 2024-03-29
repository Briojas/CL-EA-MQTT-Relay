import pytest
import adapter

job_run_id = 1
    #pubsub data
topic = '/smart-contract-client/test'
payload_string = 'test_message'
payload_float = 11.11
payload_int = 7
    #ipfs data
script_cid = 'bafybeidcuj7x347s2ekyicsu2udaime4dzwf7v5qob446pfspx3j765n7m'

def adapter_setup(test_data):
    a = adapter.Adapter(test_data)
    return a.result

#pub/sub string data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {
        'action': 'publish',
        'topic': topic, 
        'qos': 0, 
        'payload': payload_string, 
        'retain': 1
    }},
    {'id': job_run_id, 'data': {
        'action':'subscribe',
        'topic': topic, 
        'qos':0
    }}
])
def test_pub_sub_strings(test_data):
    result = adapter_setup(test_data)
    # print(result) #Debugging
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is str
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict
    if test_data['data']['action'] == 'publish':
        assert result['result']['value'] == 'published'
    else:
        assert result['result']['value'] == 'subscribed'

#pub/sub float data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {
        'action': 'publish',
        'topic': topic, 
        'qos': 0, 
        'payload': payload_float, 
        'retain': 1
    }},
    {'id': job_run_id, 'data': {
        'action':'subscribe',
        'topic': topic, 
        'qos':0
    }}
])
def test_pub_sub_floats(test_data):
    result = adapter_setup(test_data)
    # print(result) #Debugging
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is float
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict
    if test_data['data']['action'] == 'publish':
        assert result['result']['value'] == 'published'
    else:
        assert result['result']['value'] == 'subscribed'

#pub/sub int data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {
        'action': 'publish',
        'topic': topic, 
        'qos': 0, 
        'payload': payload_int, 
        'retain': 1
    }},
    {'id': job_run_id, 'data': {
        'action':'subscribe',
        'topic': topic, 
        'qos':0
    }}
])
def test_pub_sub_ints(test_data):
    result = adapter_setup(test_data)
    # print(result) #Debugging
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for topic in result['data']:
        assert type(topic['payload']['value']) is int
        assert topic['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict
    if test_data['data']['action'] == 'publish':
        assert result['result']['value'] == 'published'
    else:
        assert result['result']['value'] == 'subscribed'

#ipfs  data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {
        'action': 'ipfs',
        'topic': 'script', 
        'payload': script_cid, 
    }}
])
def test_ipfs(test_data):
    result = adapter_setup(test_data)
    # print(result) #Debugging
    assert result['statusCode'] == 200
    assert result['jobRunID'] == job_run_id
    for subtask in result['data']:
        # print(subtask)
        assert type(subtask['payload']['value']) is str
        if test_data['data']['topic'] == 'script':
            assert result['result']['value'] == 'scripted'
        assert subtask['payload']['reporting'] >= 0.5
    assert type(result['result']) is dict

#error data
@pytest.mark.parametrize('test_data', [
    {'id': job_run_id, 'data': {}},
    {'id': job_run_id, 'data': {'unknown_action': [{'fake_data': 'does_not_exist'}]}},
    {},
])
def test_error_catching(test_data):
    result = adapter_setup(test_data)
    # print(result) #Debugging
    assert result['statusCode'] == 500
    assert result['jobRunID'] == job_run_id
    assert result['error'] is not None
    assert result['status'] == 'errored'