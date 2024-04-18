import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = os.getenv("status")  # online/dnd/idle

custom_activity = {
    "name": "Playing Chipi Chipi",
    "type": 0,  # 0 for playing
    "assets": {
        "large_image": "https://c.tenor.com/Lg21skpXtU4AAAAC/cat-meme.gif",
        "large_text": "I am dumb"
    },
}

usertoken = os.getenv("token")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
    cstatus = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [custom_activity],
            "status": status,
            "afk": False,
            "buttons": [
                {"label": "My Music Bot", "url": "https://discord.com/oauth2/authorize?client_id=1200206489260933232"},
                {"label": "My Fun Bot", "url": "https://discord.com/oauth2/authorize?client_id=1218667354901315664&permissions=8&scope=applications.commands%20bot"}
            ]
        },
    }
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": "None"}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))

def run_onliner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(usertoken, status)
        time.sleep(30)

keep_alive()
run_onliner()
