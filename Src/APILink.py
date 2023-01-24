#this is a Class APILink

#trycatch over all 200

#Getdata

#Send to auction

import requests
from datetime import datetime, timedelta
import json

#Module for sending API requests to the negotiation engine.

# Perhaps import this from the config file?
API_URL = "http://127.0.0.1:5000"
TIME_OUT = 3                            # Seconds
ROOM_DURATION = 40                       # Minutes

#Create Room (POST)
#   To create the rooms(auctions) for the different blocks, done at init step of simulation
#   Pass in an object containing the necessary info: room_name, (reference_sector, reference_type), quantity, (articleno, members) 

#Auction Query (GET)
    #Want to get the status of all currently running auctions

#Join auction (GET)
    #Perhaps not strictly needed? Or have it tied into the first time a bid is placed

#Auction room (GET)

#Auction room (POST)
datasd = {
    'room_name':'test2',
    'privacy':'public',
    'members':'',
    'highest_bid':'',
    'auction_type':'Ascending',
    'closing_time':'2022-12-11T10:00:00',
    'reference_sector':'test',
    'reference_type':'test',
    'quantity':'1111',
    'templatetype':'article',
    'articleno':'22f'
}

datad = {
    'ongoing':'True'
}

#r = requests.get(API_URL+"/myrooms/admin", auth=('Elliot', ''), timeout=3) 
#r = requests.post(API_URL+"/create-room", auth=('Elliot',''), data=datasd)

#def startAuction():

#def checkWinner():

def placeBid(room_id:str, username:str, value:int):
    "Places a bid to auction <room_id> with amount <value>, returns True if successful, otherwise False"

    payload = {
        'message_input':value
    }

    r = requests.post(API_URL+"/rooms/"+room_id, auth=(username, ''), timeout=TIME_OUT, data=payload)
    if(r.status_code == 200):
        return True
    else:
        return False

def getRoomInfo(room_id:str, username:str):
    "Used to get all the auction bids placed in a specific auction room"
    r = requests.get(API_URL+"/rooms/"+room_id, auth=(username, ''), timeout=TIME_OUT)
    json_obj = r.json()                                                                     
    layer1 = str(json_obj["Bids"]).split(":", 10)                                           # Might be a weird method to get out the bidder name and amount
    name = layer1[8].split("'", 2)[1]                                                       # but it worked alright in testing so should be good seeing as this function
    value = layer1[10].split("'",2)[1]                                                      # may not even end up seeing use
    return name + ", " + value

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
        'room_name':room_name,
        'privacy':'public',
        'members':'',
        'highest_bid':'',
        'auction_type':'Ascending',
        'closing_time':current_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'reference_sector':'N/A',
        'reference_type':'N/A',
        'quantity':str(quantity),
        'templatetype':'article',
        'articleno':'N/A'
    }
    
    r = requests.post(API_URL+"/create-room", auth=(username, ''), timeout=TIME_OUT, data=payload)
    if(r.status_code == 200):
        json_obj = r.json()                     # Some formatting of the original JSON return message
        out = str(json_obj["message"])          # to only return the room id to caller
        return out.split("id: ",1)[1]
    else:
        return None