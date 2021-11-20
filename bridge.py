import paho.mqtt.client as mqtt
from typing import NamedTuple

class Bridge(object):

    def on_message(self, client, userdata, message): #pass 'self' into userdata?
        print('message: ' + message)
        for topic in self.messages:
            if topic['topic'] == message.topic:
                topic['payload'] = message.payload
                break

    def on_publish(self, client, userdata, mid):
        print('published: ' + str(mid))
        if mid == self.response['mid']:
            self.response['pending'] = False


    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('subscribed: ' + str(mid) + ' @qos: ' + str(granted_qos))
        if mid == self.response['mid']:
            self.response['pending'] = False

    def __init__(
        self,
        host,
        port,
        user = None,
        key = None,
    ):
        self.messages = []
        self.result = 'failed'
        self.reset_callback_status()
        
        self.client = mqtt.Client()

        if user and key:
            self.client.username_pw_set(user, key)
        
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe

        self.client.connect(host, port)
        self.client.loop_start()
        
    def subscribe(self, data):
        for topic in data['subscribe']['topics']:
            self.messages.append({
                'topic': topic,
                'payload': ''
            })
            response = self.client.subscribe(
                topic,
                data['subscribe']['qos']
            )
            self.response['mid'] = response[1]
            while(self.response['pending']):
                pass
            self.reset_callback_status()
        self.result = 'subscribed'

    def publish(self, data):
        for topic in data['publish']:
            self.messages.append(topic)
            response = self.client.publish(
                        topic['topic'],
                        topic['payload'],
                        topic['qos'],
                        topic['retain']
                    )
            self.response['mid'] = response[1]
            while(self.response['pending']):
                pass
            self.reset_callback_status()
        self.result = 'published'

    def reset_callback_status(self):
        self.response = {
            'pending': True,
            'mid': None
        }

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()