import paho.mqtt.client as mqtt
import time

class Bridge(object):
    def on_connect(self, client, userdata, flags, rc):
        if rc == self.response['mid']:
            self.response['pending'] = False
        else:
            self.response['error'] = rc

    def on_message(self, client, userdata, message): 
        for topic in self.messages:
            if topic['topic'] == message.topic:
                received = str(message.payload, 'UTF-8')
                try:
                    received = int(received)
                except ValueError:
                    try:
                        received = float(received)
                    except ValueError:
                        pass
                topic['payload'] = received
                break

    def on_publish(self, client, userdata, mid):
        if mid == self.response['mid']:
            self.response['pending'] = False
        else:
            self.response['error'] = mid

    def on_subscribe(self, client, userdata, mid, granted_qos):
        if mid == self.response['mid']:
            self.response['pending'] = False
        else:
            self.response['error'] = mid

    def on_disconnect(self, client, userdata, rc):
        if rc == self.response['mid']:
            self.response['pending'] = False
        else:
            self.response['error'] = rc

    def __init__(
        self,
        host,
        port,
        user = None,
        key = None,
    ):
        self.messages = []
        self.result = 'failed'
        
        self.client = mqtt.Client()

        if user and key:
            self.client.username_pw_set(user, key)
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(host, port)
        self.client.loop_start()
        self.wait_for_broker(0)
        self.disconnected = False
        
    def subscribe(self, data):
        if self.disconnected:
            self.reconnect()
        for topic in data['subscribe']['topics']:
            self.messages.append({
                'topic': topic,
                'payload': None
            })
            response = self.client.subscribe(
                topic,
                data['subscribe']['qos']
            )
            self.wait_for_broker(response[1])
        self.result = 'subscribed'

    def publish(self, data):
        if self.disconnected:
            self.reconnect()
        for topic in data['publish']:
            self.messages.append(topic)
            response = self.client.publish(
                        topic['topic'],
                        topic['payload'],
                        topic['qos'],
                        topic['retain']
                    )
            self.wait_for_broker(response[1])
        self.result = 'published'

    def wait_for_broker(self, mid):
        self.response = {
            'pending': True,
            'mid': mid,
            'error': None
        }
        wait_start = time.time()
        while(self.response['pending']):
            if time.time() - wait_start >= 3:
                #TODO: Add timeout on waiting with warning message
                print('timeout on callback response')
                break
            if self.response['error'] is not None:
                #TODO: Error handling on failing broker responses
                break
        self.response = {
            'pending': True,
            'mid': None,
            'error': None
        }

    def disconnect(self):
        self.client.disconnect()
        self.wait_for_broker(0)
        self.client.loop_stop(True)
        self.messages = []
        self.disconnected = True

    def reconnect(self):
        self.client.reconnect()
        self.client.loop_start()
        self.wait_for_broker(0)
        self.disconnected = False