import paho.mqtt as mqtt
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

    def callback(client, userdata, message):

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
        
        #self.will = Pub('',0,'',False) 
        
        self.auth = {
            'username': user,
            'password': key
        }

        self.tls = {
            'ca_certs': ca_certs,
            'certfile': cert_file,
            'keyfile': key_file,
            'tls_version': tls_version,
            'ciphers': ciphers
        }

        
    def subscribe(self, data):
        #build messages dict
        subs = Subs([],)

        #subscribe

    def publish(self, data):
        #publish
        mqtt.publish.multiple(messages,)
        #save success/failure response to messages

    #def disconnect(self):
        #disconnect from broker
