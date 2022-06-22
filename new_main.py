import websocket
import json as json
import os
import time
import rel
import _thread
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


def heartbeat_interval(ws, interval):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeat_JSON = {
                "op": 1,
                "d": "null"
        }
        on_open(ws, heartbeat_JSON)
        print("Heartbeat Sent")

   
def on_message(ws, message):
    print("This is the start of the on_message_function")
    # print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    ws.send(json.dumps(WebSocket_Config.payload))
    response = ws.recv()
    print(response)
    if response:
        return json.loads(response)
    # print("Opened connection")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WebSocket_Config.address,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    # heartbeat_interval(ws,  1000)
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()



