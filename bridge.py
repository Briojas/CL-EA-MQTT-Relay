import paho.mqtt.client as mqtt
import time

class Bridge(object):
    def on_connect(self, client, userdata, flags, rc):
        #print('on_connect ' + str(rc))
        if rc == self.callback['id']:
            self.callback['pending'] = False
        else:
            self.callback['error'] = rc
            self.callback['source'] = 'on_connect'

    def on_publish(self, client, userdata, mid):
        #print('on_pub ' + str(mid))
        if mid == self.callback['id']:
            self.callback['pending'] = False
            self.result = 'published'
        else:
            self.callback['error'] = mid
            self.callback['source'] = 'on_publish'

    def on_subscribe(self, client, userdata, mid, granted_qos):
        #print('on_sub ' + str(mid))
        if mid == self.callback['id']:
            self.callback['pending'] = False
            self.result = 'subscribed'
        else:
            self.callback['error'] = mid
            self.callback['source'] = 'on_subscribe'

    def on_disconnect(self, client, userdata, rc):
        #print('on_disconnect ' + str(rc))
        if rc == self.callback['id']:
            self.callback['pending'] = False
        else:
            self.callback['error'] = rc
            self.callback['source'] = 'on_disconnect'

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

    def __init__(
        self,
        host,
        port,
        user = None,
        key = None,
    ):
        self.messages = []
        self.result = 'failed'
        self.allowed_callback_attempts = 5
        self.allowed_callback_timeout = 5
        self.hostname = host
        
        self.client = mqtt.Client()

        if user and key:
            self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
            self.client.username_pw_set(user, key)
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

        self.await_broker_callback(
            self.client.connect,
            host, 
            port
        )
        self.client.loop_start()
        self.disconnected = False
        
    def subscribe(self, data):
        if self.disconnected:
            self.reconnect()
        self.messages.append({
            'topic': data['topic'],
            'payload': None
        })
        self.await_broker_callback(
            self.client.subscribe,
            data['topic'],
            data['qos']
        )

    def publish(self, data):
        if self.disconnected:
            self.reconnect()
        self.messages.append({
            'topic': data['topic'],
            'payload': data['payload']
        })
        self.await_broker_callback(
            self.client.publish,
            data['topic'],
            data['payload'],
            data['qos'],
            data['retain']
        )

    def disconnect(self):
        self.await_broker_callback(self.client.disconnect)
        self.client.loop_stop()
        self.messages = []
        self.disconnected = True

    def reconnect(self):
        self.await_broker_callback(self.client.reconnect)
        self.client.loop_start()
        self.disconnected = False

    def await_broker_callback(self, action, *params):
        curr_attempts = 1
        while(curr_attempts <= self.allowed_callback_attempts):
            id = action(*params)
            if type(id) is not int:
                id = id[1] 
            if self.client._thread is None:
                self.client.loop_start() #loop needs to be running for callbacks to respond
            self.callback = {
                'pending': True,
                'id': id,
                'error': None,
                'source': None
            }
            retry = False
            wait_start = time.time()
            while(self.callback['pending']):
                if time.time() - wait_start >= self.allowed_callback_timeout:
                    #TODO: Add timeout message logging
                    print('callback timeout on host: ' + self.hostname)
                    retry = True
                    break
                if self.callback['error'] is not None:
                    #TODO: Error handling on failing broker responses
                    print('callback type: ' + self.callback['source'] + ' error: ' + str(self.callback['error']) + ' @host: ' + self.hostname)
                    break
            if not retry:
                break
            curr_attempts = curr_attempts + 1
        self.callback = {
            'pending': True,
            'id': None,
            'error': None,
            'source': None
        }