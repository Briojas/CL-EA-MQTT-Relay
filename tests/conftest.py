import pytest

job_run_id = 1 #will increment for each job created
    #pubsub raw data
pub_data = [
    {
        'topic': '/test_data_string',
        'payload': 'test',
        'jobs': []
    },{
        'topic': '/test_data_float',
        'payload': 0.5,
        'jobs': []
    },{
        'topic': '/test_data_int',
        'payload': 1,
        'jobs': []
    }]
sub_data = pub_data
    #ipfs raw data
ipfs_script_cids = [
    'bafybeifuzupfst7soyc7oe2hiilgvm7h6m2myu5tk37dth3nm7c2ifrqqm'
]
    #pub jobs
jobs_pub_strings = {}
jobs_pub_floats = {}
jobs_pub_ints = {}
    #sub jobs
jobs_sub_strings = {}
jobs_sub_floats = {}
jobs_sub_ints = {}
    #ipfs jobs
jobs_ipfs_scripts = {}
    #errors jobs
jobs_error = {}

@pytest.fixture
def jobs_pub_strings():
    return pub_jobs(str)
@pytest.fixture
def jobs_pub_floats():
    return pub_jobs(float)
@pytest.fixture
def jobs_pub_ints():
    return pub_jobs(int)
@pytest.fixture
def jobs_sub_strings():
    return sub_jobs(str)
@pytest.fixture
def jobs_sub_floats():
    return sub_jobs(float)
@pytest.fixture
def jobs_sub_ints():
    return sub_jobs(int)
@pytest.fixture
def jobs_ipfs_scripts():
    return ipfs_jobs('script')
@pytest.fixture
def error_jobs():
    global jobs_error
    global job_run_id
    jobs_error = [
        {'id': job_run_id + 1,'data': {}},
        {'id': job_run_id + 2,'data': {'unknown_action': [{'fake_data': 'does_not_exist'}]}},
        {}]
    return jobs_error  

def pub_jobs(test_data_type):
    global job_run_id
    global pub_data
    global jobs_pub_strings
    global jobs_pub_floats
    global jobs_pub_ints
        #pub job construction
    for data_type in pub_data:
        data_type['jobs'].append(job_constructor('publish', pubsub_data_tuples('publish',data_type['topic'],data_type['payload'])))
        #pub job organization
    jobs_pub_strings = pub_data[0]['jobs']
    jobs_pub_floats = pub_data[1]['jobs']
    jobs_pub_ints = pub_data[2]['jobs']

    if test_data_type is str:
        return jobs_pub_strings
    if test_data_type is float:
        return jobs_pub_floats
    if test_data_type is int:
        return jobs_pub_ints

def sub_jobs(test_data_type):
    global sub_data
    global jobs_sub_strings
    global jobs_sub_floats
    global jobs_sub_ints
        #sub job construction
    for data_type in sub_data:
        data_type['jobs'].append(job_constructor('publish', pubsub_data_tuples('subscribe',data_type['topic'],data_type['payload'])))
        #sub job organization
    jobs_sub_strings = sub_data[0]['jobs']
    jobs_sub_floats = sub_data[1]['jobs']
    jobs_sub_ints = sub_data[2]['jobs']

    if test_data_type is str:
        return jobs_pub_strings
    if test_data_type is float:
        return jobs_pub_floats
    if test_data_type is int:
        return jobs_pub_ints

def ipfs_jobs(subtask):
    global ipfs_script_cids
    global jobs_ipfs_scripts
        #ipfs job construction
    jobs_ipfs_scripts = job_constructor('ipfs', ipfs_data_tuples('subtask', ipfs_script_cids))
    if subtask is 'script':
        return jobs_ipfs_scripts

def pubsub_data_tuples(self, action, payload_specific_topic, payload):
        #data definitions
    tuples = []
    main_topic = '/cl-ea-mqtt-client'
    qos_topics = ['/low', '/med', '/high']
    qos_values = {
        '/low':0,
        '/med':1,
        '/high':2}
    retain_topics = ['/unretained', '/retained']
    retain_values = {
        '/unretained':0,
        '/retained':1}

    for qos_topic in qos_topics:
        for retain_topic in retain_topics:
            topic = main_topic + payload_specific_topic + qos_topic + retain_topic
            qos = qos_values[qos_topic]
            retain = retain_values[retain_topic]
            if action is 'publish':
                tuples.append((
                    topic,
                    qos,
                    payload,
                    retain))
            else:
                tuples.append((
                    topic,
                    qos,
                    None,
                    None))
    return tuples

def ipfs_data_tuples(self, subtask, cids):
    tuples = []
    for cid in cids:
        tuples.append((
            subtask,
            None,
            cid,
            None))
    return tuples

def job_constructor(self, action, data_tuples):
    builtJobs = []
    for job_tuple in data_tuples:
        builtJobs.append(
            {
                'id': job_run_id,
                'data': {
                    'action': action,
                    'topic': job_tuple[0], 
                    'qos': job_tuple[1], 
                    'payload': job_tuple[2], 
                    'retain': job_tuple[3]
                }
            }
        )
        job_run_id = job_run_id + 1
    return builtJobs