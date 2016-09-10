from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import json

def gen_msg():
    msg = {'type': 'subscription'}
    msg['deviceName'] = 'openbci'
    msg['deviceId'] = 'octopicorn'
    msg['metric'] = 'heart_rate'
    json_msg = json.dumps(msg)
    return json_msg


class WSClient(TornadoWebSocketClient):
    def opened(self):
        msg = gen_msg()
        self.send(msg)

    def received_message(self, m):
        print m
        if len(m) == 175:
            self.close(reason='Bye bye')

    def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()

ws = WSClient('ws://node6.getcloudbrain.com:31415/rt-stream/websocket', protocols=['http-only', 'chat', 'websocket'])
ws.connect()

ioloop.IOLoop.instance().start()
