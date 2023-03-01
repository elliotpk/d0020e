# Library / Module containing necessary functions to communicate with the API, abstracted into this module to keep the rest of the simulation more clear.

import requests
from datetime import datetime, timedelta
import json

# Module for sending API requests to the negotiation engine.

# Perhaps import this from the config file?
API_URL = "http://127.0.0.1:5000"
TIME_OUT = 1                            # Seconds
ROOM_DURATION = 5                       # Minutes

def endAuction(room_id:str, username:str, winner:str):
    "Used to decide on a winner for the auction, username needs to be the admin for the auction and winner the username of the person who won"
    r = requests.post(API_URL+"/rooms/"+room_id+"/end", auth=(username, ''), data={"winner":winner})
    return r.text

def getWinner(room_id:str, username:str):
    "Used to get the winner of an auction after it has ended"
    r = requests.get(API_URL+"/rooms/"+room_id+"/end", auth=(username, ''))
    return r.text

def placeBid(room_id:str, username:str, value:int):
    "Places a bid to auction <room_id> with amount <value>, returns True if successful, otherwise False"

    r = requests.post(API_URL+"/rooms/"+room_id, auth=(username, ''), timeout=TIME_OUT, data={'message_input':value})
    if(r.status_code == 200):
        return True
    else:
        return False

def getRoomInfo(room_id:str, username:str, order:str):
    """
    Used to get all the auction bids placed in a specific auction room. 
    Can order the list by time (order = 'time') or bid amount (order = 'bid')
    """
    r = requests.get(API_URL+"/rooms/"+room_id, auth=(username, ''), timeout=TIME_OUT)
    if(r.status_code != 200):
        print("Error")
        return
        
    json_obj = r.json()                                                                     
    value = json_obj["Bids"]
    output = []
    if(len(value) == 0):
        output.append({"room_id" : room_id, "user" : 'N/A', "value" : 0})   # Incase there are no bids in the auction, usually when simulation has just started
    else:
        for entry in value:
            output.append({"room_id" : room_id, "user" : entry["sender"]["val"][0], "value" : int(entry["text"]["val"][0])})
    sort = False
    if(order == "bid"):
        sort = True

    return sorted(output, key=lambda i:int(i['value']), reverse=sort)

def addUser(room_id:str, username:str):
    r = requests.get(API_URL+"/rooms/"+room_id+"/join", auth=(username, ''), timeout=TIME_OUT)
    if(r.status_code==200):
        return True
    else:
        return False

def createAuction(room_name:str, username:str, quantity:int):
    "Posts an auction to the database and returns the Room ID if successful, otherwise None"

    current_time = datetime.now() + timedelta(minutes=ROOM_DURATION)
    payload = {
        'room_name': room_name,
        'privacy': 'public',
        'members': '',
        'highest_bid': '',
        'auction_type': 'Ascending',
        'closing_time': current_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'reference_sector': 'N/A',
        'reference_type': 'N/A',
        'quantity': str(quantity),
        'templatetype': 'article',
        'articleno': 'N/A'
    }
    
    r = requests.post(API_URL+"/create-room", auth=(username, ''), timeout=TIME_OUT, data=payload)
    if(r.status_code == 200):
        json_obj = r.json()                     # Some formatting of the original JSON return message
        out = str(json_obj["message"])          # to only return the room id to caller
        return out.split("id: ",1)[1]
    else:
        return None