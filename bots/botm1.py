import sys, os
import time

filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

### Setup
parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print('---')
time.sleep(2) # Sleep to avoid API rate limit

print(json.loads(client.meeting.list(user_id="me").content))
time.sleep(2) # Sleep to avoid API rate limit
response = json.loads(client.chat_channels.list().content)
print(response)
channels = response["channels"]
print(channels)

for c in channels:
    print(c)
    if "my_test" in c.values():
        print("Found channel my_test", c["id"])
        cid = to_channel = c["id"]

# Send message
stop = False
while not stop:
    message = input("Enter message: ")
    print(client.chat_messages.post(to_channel=cid, message=message))
    if message == "stop":
        stop = True

# List message
messageList = json.loads(client.chat_messages.list(to_channel=cid, user_id="me").content)["messages"]
time.sleep(1) # Sleep to avoid API rate limit

# Update a message
print(client.chat_messages.update(to_channel=cid, messageId=messageList[0]["id"], message="I've been edited"))
time.sleep(2) # Sleep to avoid API rate limit

# Delete a message
print(client.chat_messages.delete(to_channel=cid, messageId=messageList[0]["id"]).content)
