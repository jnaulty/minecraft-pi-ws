#!/usr/bin/python
from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import json
import ast

heart_rate = 0

def subscribe():
    msg = {'type': 'subscription'}
    msg['deviceName'] = 'openbci'
    msg['deviceId'] = 'octopicorn'
    msg['metric'] = 'heart_rate'
    json_msg = json.dumps(msg)
    return json_msg

def convert_msg_to_dict(m):
    global heart_rate
    msg = m.data.decode("utf-8")
    msg_dict = ast.literal_eval(msg)
    heart_rate = msg_dict["bpm"]
    return msg_dict

class WSClient(TornadoWebSocketClient):
    def opened(self):
        msg = subscribe()
        self.send(msg)

    def received_message(self, m):
        #print m
        msg = convert_msg_to_dict(m)
        print msg
        if len(m) == 175:
            self.close(reason='Bye bye')

    def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()

def start():
    WS_SERVER='ws://node6.getcloudbrain.com:31415/rt-stream/websocket'
    ws = WSClient(WS_SERVER, protocols=['http-only', 'chat', 'websocket'])
    ws.connect()
    
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start()
