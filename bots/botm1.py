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


def get_channel(cid):
    getchannel = json.loads(client.chat_channels.get(channelId=cid).content)
    try:
        print(getchannel)
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


def send_message(message, cid):
    print(client.chat_messages.post(to_channel=cid, message=message))

def edit_message(messageId, cid, message):
    print(client.chat_messages.update(to_channel=cid, messageId=messageId, message=message))

def delete_message(messageId, cid):
    print(client.chat_messages.delete(to_channel=cid, messageId=messageId).content)

def create_channel(name, typeOf, members):
    print(client.chat_channels.create(name=name, type=typeOf, members=members))

def update_channel(cid, name):
    print(client.chat_channels.update(channelId=cid, name=name).content)

def leave_channel(cid):
    print(client.chat_channels.leave(channelId=cid).content)

def join_channel(cid):
    print(client.chat_channels.join(channelId=cid).content)

def delete_channel(cid):
    print(client.chat_channels.delete(channelId=cid).content)

def remove_member(cid, memberId):
    print(client.chat_channels.remove(channelId= cid, memberId = memberId).content)

def invite_member(cid, email):
    print(client.chat_channels.invite(channelId = cid, members = email).content)

def list_members(cid):
    list_mem = json.loads(client.chat_channels.list_members(channelId=cid).content)
    try:
        for member in list_mem["members"]:
            print(member["name"])
            print("ID: " + member["id"])
            print("")
    except KeyError:
        print(ERROR_MSG)


ACTIONS = [
    "0. Exit program",
    "1. See existing channels",
    "2. See channel detail",
    "3. Create a new channel",
    "4. List last 10 messages in channel",
    "5. Send message to channel",
    "6. Edit message in channel",
    "7. Delete message in channel",
    "8. Edit channel name",
    "9. Delete channel",
    "10. List members of channel",
    "11. Join channel",
    "12. Leave channel",
    "13. Remove member from channel",
    "14. Invite member(s) to channel"
]

ERROR_MSG = "Something went wrong while trying to perform this action. Please make sure the input was valid and your " \
            "network connection is stable. "


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
            cid = input("Enter channel id: ")
            get_channel(cid)
        elif action == 3:
            name = input("Enter name of channel: ")
            typeOf = input("Enter type of channel (1 private, 2 private, 3 public): ")
            members = []
            create_channel(name,typeOf,members)
        elif action == 4:
            cid = input("Enter channel id: ")
            list_messages(cid)
        elif action == 5:
            cid = input("Enter channel id: ")
            msg = input("Enter message: ")
            send_message(msg, cid)
        elif action == 6:
            cid = input("Enter channel id: ")
            msg_id = input("Enter message id: ")
            msg = input("Enter message: ")
            edit_message(msg_id, cid, msg)
            pass
        elif action == 7:
            cid = input("Enter channel id: ")
            msg_id = input("Enter message id: ")
            delete_message(msg_id, cid)
            pass
        elif action == 8:
            cid = input("Enter channel id: ")
            name = input("Enter new channel name: ")
            update_channel(cid, name)
            pass
        elif action == 9:
            cid = input("Enter channel id: ")
            delete_channel(cid)
            pass
        elif action == 10:
            cid = input("Enter channel id: ")
            list_members(cid)
            pass
        elif action == 11:
            cid = input("Enter channel id: ")
            join_channel(cid)
            pass
        elif action == 12:
            cid = input("Enter channel id: ")
            leave_channel(cid)
            pass
        elif action == 13:
            cid = input("Enter channel id: ")
            memberId = input("Enter member id: ")
            remove_member(cid, memberId)
            
            pass
        elif action == 14:
            cid = input("Enter channel id: ")
            email = input("Enter email to invite: ")
            members = [{"email":email}]
            invite_member(cid, members)
            pass
        else:
            print("Please enter a number between 1 to " + str(len(ACTIONS) - 1))
    except ValueError:
        print("Action not recognized. Please enter a number from 1 to " + str(len(ACTIONS) - 1))
    print("\n---------------------\n")

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
