import websocket
import json as json
import os
from dotenv import load_dotenv

class Websocket_Config:

    # Standard enviornment variables and general object creation
    load_dotenv()
    botToken = os.getenv("botToken")
    ws = websocket.WebSocket()
    
    # Payload information
    payload = {
        "op": 2,
        "d": {
            "token": botToken,
            "intents": 513,
            "properties": {
                "$os": "linux",
                "$browser": "chrome",
                "$device": "pc"
            }
        }
    }


    def __init__(self, request, response):
        self.request = request
        self.response = response


    def request_json(ws):
        Websocket_Config.request = ws.send(json.dumps(Websocket_Config.payload))
        


    def receive_json(ws):
        Websocket_Config.response = ws.recv()
        if Websocket_Config.response:
            return json.loads(Websocket_Config.response)


def main():
    
    request = Websocket_Config.request_json(Websocket_Config.ws)
    print(request)
    '''
    response = Websocket_Config.response()
    if response:
        print(response)
    '''

'''
def send_json_request(websocket, request):
    websocket.send(json.dumps(request))

def receive_json_response(websocket):
    response = websocket.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, websocket):
    print("Heartbeat Begin")
    while True:
        time.sleep(interval)
        heartbeat_json = {
                "op": 1,
                "d": "null"
        }
        send_json_request(websocket, heartbeat_json)
        print("Heartbeat Sent")

'''

if __name__ == "__main__":
    main()
