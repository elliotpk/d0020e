#this is a Class APILink

#trycatch over all 200

#Getdata

#Send to auction

import requests

#Module for sending API requests to the negotiation engine.

# Perhaps import this from the config file for ease of use?
API_URL = "http://127.0.0.1:5000"

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

r = requests.get(API_URL+"/myrooms/admin", auth=('Elliot', ''), timeout=3) 
#r = requests.post(API_URL+"/create-room", auth=('Elliot',''), data=datasd)

print(r.text)
if r:
    print("yep")
else:
    print("nope")