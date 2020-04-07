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
    if "my_test" in c.values():
        #print("Found channel my_test", c["id"])
        cid = to_channel = c["id"]
cid = to_channel
# Send message
# stop = False
# while not stop:
#     message = input("Enter message: ")
#     print(client.chat_messages.post(to_channel=cid, message=message))
#     if message == "stop":
#         stop = True
# 
#
# print("-------Channel List-------")
# channelList = json.loads(client.chat_channels.list(to_channel=cid).content)["channels"]
# time.sleep(2)
# print(channelList)
#
# print("-------Get Channel--------")
# getchannel = json.loads(client.chat_channels.get(channelId = cid).content)
# time.sleep(2)
# print(getchannel)
# time.sleep(2)
time.sleep(2)
print("-------Get Members--------")
member = json.loads(client.chat_channels.list_members(channelId = cid).content)["members"][0]
time.sleep(2)
print(member)
print(member["email"])

for c in channels:
    if "Edited Channel Name" in c.values():
        #print("Found channel my_test", c["id"])
        cid = to_channel = c["id"]
time.sleep(2)

invites = [{"email": member["email"]}]
print("--------Invite Member----------")
print(client.chat_channels.invite(channelId = cid, members = invites).content)

time.sleep(2)
print("------Remove a Member-------")
print(client.chat_channels.remove(channelId = cid, memberId = member["id"]).content)

# time.sleep(2)
# print("---------Create Channel---------")
# email = json.loads(client.user.get(id = "me").content)["email"]
# name = "Hello World"
# typeOf = 1
# members = [{"email": email}]
#
# time.sleep(2)
# obj= json.loads(client.chat_channels.create(name= name, type=typeOf, members=members).content)
# cid = obj["id"]
# print(obj)
#
# print("-------Get Members--------")
# list_mem = json.loads(client.chat_channels.list_members(channelId = cid).content)["members"]
# time.sleep(2)
# print(list_mem)

# print("--------------Update Channel----------")
# print(client.chat_channels.update(channelId=cid, name="Edited Channel Name").content)
# time.sleep(2)

# print("--------Delete Channel-------")
# print(client.chat_channels.delete(channelId=cid).content)
# time.sleep(2)

# print(client.chat_messages.update(to_channel=cid, messageId=messageList[0]["id"], message="I've been edited"))

# time.sleep(2)
# print("----Leave Channel----")
# print(client.chat_channels.leave(channelId = cid).content)


# time.sleep(2)
# print("------Join Channel---")
# jsonObject = json.loads(client.chat_channels.join(channelId = cid).content) 
# print(jsonObject)
# id = jsonObject["id"] 
# time_added = jsonObject["added_at"] 
# print(id + " was added at " + time_added)


# # List message
# messageList = json.loads(client.chat_messages.list(to_channel=cid, user_id="me").content)["messages"]
# time.sleep(1) # Sleep to avoid API rate limit

# # Update a message
# print(client.chat_messages.update(to_channel=cid, messageId=messageList[0]["id"], message="I've been edited"))
# time.sleep(2) # Sleep to avoid API rate limit

# # Delete a message
# print(client.chat_messages.delete(to_channel=cid, messageId=messageList[0]["id"]).content)
