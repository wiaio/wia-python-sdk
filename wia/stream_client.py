import paho.mqtt.client as mqtt
import wia
import threading
import resource
import json
import re
import sys

client = mqtt.Client()
function_subscriptions = {}

class Stream(object):
    connected = False
    subscribed = None
    subscribed_count = 0

    @classmethod
    def connect(self):
        global client
        client.username_pw_set(wia.secret_key, ' ')
        client.on_connect = Stream.on_connect
        client.on_disconnect = Stream.on_disconnect
        client.on_subscribe = Stream.on_subscribe
        client.on_unsubscribe = Stream.on_unsubscribe
        client.on_message = Stream.on_message
        client.connect(wia.stream_host, wia.stream_port, 60)
        client.loop_start()

    @classmethod
    def disconnect(self):
        global client
        client.loop_stop()
        client.disconnect()

    @classmethod
    def publish(self, **kwargs):
        topic = kwargs['topic']
        kwargs.pop('topic')
        client.publish(topic, payload=json.dumps(kwargs), qos=0, retain=False)

    @classmethod
    def subscribe(self, **kwargs):
        function_subscriptions[kwargs['topic']] = kwargs['func']
        def thread_proc():
            client.subscribe(kwargs['topic'], qos=0)
            subscribing_event = threading.Event()
        t = threading.Thread(group=None, target=thread_proc, name=None)
        t.run()

    @classmethod
    def unsubscribe(self, **kwargs):
        function_subscriptions.pop(kwargs['topic'])
        topic = kwargs['topic']
        client.unsubscribe(topic)

    @classmethod
    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        print("Connect success")

    @classmethod
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("Disconnect success")

    @classmethod
    def on_subscribe(self, client, userdata, msg, granted_qos):
        self.subscribed = True
        self.subscribed_count += 1
        print("Subscribe success")

    @classmethod
    def on_message(self, client, userdata, msg):
        topic=re.split('/', msg.topic)
        # 1. Check for specific topic function. If exists, call
        if msg.payload:
            if msg.topic in function_subscriptions:
                payload = json.loads(msg.payload.decode())
                payload = dict([(str(k), v) for k, v in payload.items()])
                for k, v in payload.items():
                    if int(sys.version_info[0]) >=3:
                        if isinstance(v, bytes):
                            payload[k] = str(v)
                    else:
                        if isinstance(v, unicode):
                            payload[k] = str(v)
                function_subscriptions[msg.topic](payload)
        else:
            if msg.topic in function_subscriptions:
                function_subscriptions[msg.topic](None)
        # 2. Check for wildcard topic function. If exists, call
        wildcard_topic = topic[0] + "/" + topic[1] + "/" + topic[2] + "/+"
        if msg.payload:
            if wildcard_topic in function_subscriptions:
                if hasattr(function_subscriptions[wildcard_topic], '__call__'):
                    payload = json.loads(msg.payload.decode())
                    payload = dict([(str(k), v) for k, v in payload.items()])
                    for k, v in payload.items():
                        if int(sys.version_info[0]) >=3:
                            if isinstance(v, bytes):
                                payload[k] = str(v)
                        else:
                            if isinstance(v, unicode):
                                payload[k] = str(v)
                    function_subscriptions[wildcard_topic](payload)
        else:
            if wildcard_topic in function_subscriptions:
                function_subscriptions[wildcard_topic](None)

    @classmethod
    def on_unsubscribe(self, client, userdata, mid):
        self.subscribed_count -= 1
        if self.subscribed_count == 0:
            self.subscribed = False
        print("Unsubscribe success")
