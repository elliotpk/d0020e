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
ROOM_DURATION = 5                       # Minutes

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

#def placeBids(room_id):
    #command = "/rooms/" + room_id
    #required payload: username, message_input (bid amount), 
    #requests.post()....
    #catch 404
  
def createAuction(room_name:str, username:str, quantity:int):
    "Posts an auction to the database and returns the Room ID if successful, otherwise None."

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
        json_obj = r.json()
        out = str(json_obj["message"])
        return out.split("id: ",1)[1]
    else:
        return None