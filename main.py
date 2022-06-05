'''
Copyright 2022 VikingOfValhalla

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT 
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.
'''

import websocket
import json
import os
import requests
import threading
import time




# other files
from commands import *
from server_rules import *
from get_help import *
from rand_proj import *
from dotenv import load_dotenv
from dice_roll import *
from news_api import *

load_dotenv()

botToken = os.getenv('botToken')


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("heartbeat sent")


ws = websocket.WebSocket()

ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

event = receive_json_response(ws)


heartbeat_interval = event["d"]["heartbeat_interval"] / 1000

threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

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

send_json_request(ws, payload)

while True:

    event = receive_json_response(ws)

    message_header = {"authorization": "Bot {}".format(botToken)}

    try:
        content = event['d']['content']
        author = event['d']['author']['username']
        channelID = event['d']['channel_id']

        # / command for sending message data
        if content.startswith("/"):
            print(f'{author}: {content}')

            if content == "/server_rules":
                message_content = {"content": f'{server_rules_message}'}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content == "/help":
                message_content = {"content": f'{get_help_message}'}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content == "/commands":
                message_content = {"content": command_list_function(command_list)}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content == "/random_project":
                message_content = {"content": compile_list(programming_task)}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content == "/dice_roll":
                message_content = {"content": dice_roll_function()}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content == "/news":
                message_content = {"content": articles}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

            if content not in command_list:
                message_content = {
                    "content": '''Hmmm... I don't think I know that command. Try using "/commands" to see a full list of commands'''}
                post_message = requests.post("https://discord.com/api/v6/channels/{}/messages".format(channelID),
                                             data=message_content, headers=message_header)

    except:
        pass

asyncio.get_event_loop().run_until_compelte(ws)
