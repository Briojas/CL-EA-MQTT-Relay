import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from typing import NamedTuple

class Subs(NamedTuple):
    topics: list
    qos: int

class Pub(NamedTuple):
    topic: str
    qos: int
    payload: str
    retain: bool

class Bridge(object):

    messages = []

    def callback(self, client, userdata, message):
        for topic in self.messages:
            if topic['topic'] == message.topic:
                topic['payload'] = message.payload
                break

    def __init__(
        self,
        host,
        port,
        user = None,
        key = None,
        ca_certs = None,
        cert_file = None,
        key_file = None,
        tls_version = None,
        ciphers = None
    ):
        self.host = host
        self.port = port
        
        #self.will = Pub('',0,'',False) #not implemented

        self.auth = None
        if user and key:
            self.auth = {
                'username': user,
                'password': key
            }

        self.tls = None
        if ca_certs: #only ca_certs needed for tls
            self.tls = {
                'ca_certs': ca_certs,
                'certfile': cert_file,
                'keyfile': key_file,
                'tls_version': tls_version,
                'ciphers': ciphers
            }

        
    def subscribe(self, data):
        subs = Subs(data['subscribe']['topics'],data['subscribe']['qos'])
        for topic in subs.topics:
            self.messages.append({
                'topic': topic,
                'payload': ''
            })
        
        subscribe.callback(
            self.callback, 
            subs.topics, 
            subs.qos, 
            hostname = self.host,
            port = self.port,
            auth = self.auth,
            tls = self.tls
        )

        self.messages.append({
            'status': 'subscribed'
        })


    def publish(self, data):
        
        for topic in data['publish']:
            self.messages.append(
                Pub(
                    topic['topic'],
                    topic['qos'],
                    topic['payload'],
                    topic['retain']
                )
            )
        
        publish.multiple(
            self.messages,
            hostname=self.host,
            port=self.port,
            auth=self.auth,
            tls=self.tls
        )
        
        self.messages.append({
            'status': 'published'
        })