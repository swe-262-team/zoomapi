import sys, os
from enum import Enum
import time

filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok


def setup():
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
    return client


def list_channels(client):
    response = json.loads(client.chat_channels.list().content)
    try:
        channels = response["channels"]
        for channel in channels:
            print(channel["name"] + ": " + channel["id"])
    except KeyError:
        print(ERROR_MSG)


def list_messages(cid):
    try:
        messageList = json.loads(client.chat_messages.list(to_channel=cid, user_id="me").content)["messages"]
        print("")
        for message in messageList:
            print("From: " + message["sender"])
            print("Message ID: " + message["id"])
            print(message["message"])
            print("")
    except KeyError:
        print(ERROR_MSG)


def send_message(client, message, cid):
    print(client.chat_messages.post(to_channel=cid, message=message))


def edit_message(client, messageId, cid, message):
    print(client.chat_messages.update(to_channel=cid, messageId=messageId, message=message))


def delete_message(client, messageId, cid):
    print(client.chat_messages.delete(to_channel=cid, messageId=messageId).content)

ACTIONS = [
    "0. Exit program",
    "1. See existing channels",
    "2. Create a new channel",
    "3. List last 10 messages in channel",
    "4. Send message to channel",
    "5. Edit last message in channel",
    "6. Delete last message in channel",
    "7. Edit channel name",
    "8. Delete channel",
    "9. List members of channel",
    "10. Join channel",
    "11. Leave channel",
    "12. Remove member from channel",
    "13. Invite member(s) to channel"
]

ERROR_MSG = "Something went wrong while trying to perform this action"


def display_prompt():
    print("Please enter a number from the following options:")
    for action in ACTIONS:
        print(action)


### Run
client = setup()

usr_input = ""
while usr_input != "0":
    display_prompt()
    usr_input = input("\nEnter number: ")
    print("")
    try:
        action = int(usr_input)
        if action == 0:
            pass
        elif action == 1:
            list_channels(client)
        elif action == 2:
            # create channel
            pass
        elif action == 3:
            cid = input("Enter channel id: ")
            list_messages(cid)
        elif action == 4:
            cid = input("Enter channel id: ")
            msg = input("Enter message: ")
            send_message(client, msg, cid)
        elif action == 5:
            cid = input("Enter channel id: ")
            msg_id = input("Enter message id: ")
            msg = input("Enter message: ")
            edit_message(client, msg_id, cid, msg)
            pass
        elif action == 6:
            cid = input("Enter channel id: ")
            msg_id = input("Enter message id: ")
            delete_message(client, msg_id, cid)
            pass
        elif action == 7:
            # update channel name
            pass
        elif action == 8:
            # delete channel
            pass
        elif action == 9:
            # list members of channel
            pass
        elif action == 10:
            # join channel
            pass
        elif action == 11:
            pass
        elif action == 12:
            pass
        elif action == 13:
            pass
        elif action == 14:
            pass
        else:
            print("Please enter a number between 1 to " + str(len(ACTIONS)-1))
    except ValueError:
        print("Action not recognized. Please enter a number from 1 to " + str(len(ACTIONS) - 1))
    print("\n---------------------\n")


#
# print("-------Channel List-------")
# channelList = json.loads(client.chat_channels.list(to_channel=cid).content)["channels"]
# time.sleep(2)
# print(channelList)
#
# print("-------Get Channel--------")
# getchannel = json.loads(client.chat_channels.get(channelId=cid).content)
# time.sleep(2)
# print(getchannel)
# time.sleep(2)
# print("-------Get Members--------")
# list_mem = json.loads(client.chat_channels.list_members(channelId=cid).content)["members"]
# time.sleep(2)
# print(list_mem)
#
# time.sleep(2)
# print("----Leave Channel----")
# print(client.chat_channels.leave(channelId=cid).content)
#
# time.sleep(2)
# print("------Join Channel---")
# jsonObject = json.loads(client.chat_channels.join(channelId=cid).content)
# print(jsonObject)
# id = jsonObject["id"]
# time_added = jsonObject["added_at"]
# print(id + " was added at " + time_added)
