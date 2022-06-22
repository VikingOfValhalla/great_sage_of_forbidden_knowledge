import websocket
import json as json
import os
import time
import requests
import threading
from dotenv import load_dotenv


class WebSocket_Config:
    # Standard enviornment variables and general object creation
    load_dotenv()
    botToken = os.getenv("botToken")
    address = "wss://gateway.discord.gg/?v=6&encoding=json"

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


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat_interval(ws, interval):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeat_JSON = {
                "op": 1,
                "d": "null"
        }
        send_json_request(ws, heartbeat_JSON)
        print("Heartbeat Sent")


if __name__ == "__main__":
    # Main settings
    websocket.enableTrace(True)
    ws = websocket.WebSocket()
    ws.connect(WebSocket_Config.address)

    # Receive, Heartbeat, and Send
    event = receive_json_response(ws)
    heartbeat_interval_time = event["d"]["heartbeat_interval"] / 1000
    threading._start_new_thread(heartbeat_interval, (ws, heartbeat_interval_time))
    send_json_request(ws, WebSocket_Config.payload)
    
    try:
        while True:
            event = receive_json_response(ws)    
            message_header = {"authorization": "Bot {}".format(WebSocket_Config.botToken)}
            print(event["d"])

    except Exception as e:
        print(e)


