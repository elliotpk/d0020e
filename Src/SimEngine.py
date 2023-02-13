import APILink as link
from Bidder import *
from Sellers import Sellers
import random

import os
def printdata(string):
    #spara data före print
    #prints the results into a csv file and labels the different runs into a new csv file
    testnr = 0
    while (os.path.exists('test'+str(testnr)+'.csv')):
        testnr=testnr+1
    print(testnr)
    mkcsv = open('test'+str(testnr)+'.csv','w')
    for x in string.split(';'):
        mkcsv.write(x+'\n')
    mkcsv.close()
""""
pris,data,vinnare,id
1,sten,34,#91
420,lera,2,#54
"""
#print(Api.data) print to csv-file

class SimEngine():
    def __init__(self, sellers, buyers):
        END_THRESHOLD = 2                                                           # How many rounds of inactive to keep an auction running for
        self.sellers = sellers
        self.Buyers = buyers
        self.auctions = self.createAuctionList(self.sellers, self.auctionStatus)    # Create a list of all auctions
        self.auctionStatus = self.createAuctionStatus(self.auctions)                # Used to keep track of when a bid has not been placed recently (within x loops)
        self.finished = []                                                          # Auctions which have ended are placed here
        self.buyers = buyers
        if(not self.addBuyers(self.buyers)):                                        # Error checking if adding buyers to auctions went well
            return None


    def simStart(self):
        "Start the simulation"
        #Round Start
        while(len(self.auctions) > 0):
            # Update the auction list with current values
            for auction in self.auctions:
                info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]   # Get highest bid in the auctions, auth is 'Seller' for all auctions in the current implementation
                auction['top_bid'] = info['value']
                auction['user'] = info['user']
            
            
            # Send updated auction list to buyers and wait for their decision
            newBids = []
            for buyer in self.buyers:
                temp = buyer.bidUpdate(self.auctions)
                newBids.append(temp)

            finished = []
            for auction in self.auctions:
                bids = []
                for buyers in newBids:
                    t = next((item for item in buyers if item["id"] == auction["id"]), None)                  # Extracts all the bids for each auction ID
                    if(t != None):
                        bids.append(t)
                sort = sorted(bids, key=lambda i:int(i['value']), reverse=True)                               # Sorts the list of bids by amount
                # !! Pass the list "sort" to the datamanagement class here !!
                max_bid = sort[0]['value']
                top = []
                for i in range(len(sort), 0, -1):                                                             # Pick out any potential ties for the top bid to randomize which one gets submitted
                    if(int(sort[i]['value']) == int(max_bid)):
                        top.append(sort.pop(i))
                print("New top bid of: "+ str(sort[0]['value']) +" submitted for auction: " + auction['id'] + " by user: " + sort[0]['user'])
                finished.append(random.choice(top))                                                           # random.choice selects a random auction from the list

            for id in finished:
                for bid in id:
                    r = link.placeBid(bid['id'], bid['user'], bid['value'])
                    if(not r):
                        print('Error when placing the bid for user: ' + bid['user'] + ' to auction: ' + bid['id'])
        
        # Update the auction list with the final result
        for auction in self.auctions:
            info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]
            auction['top_bid'] = info['value']
            auction['user'] = info['user']

    def endAuction(self, auction):
        "Called to end the specific auction"
        link.endAuction(auction['id'], 'Seller', auction['user'])
        self.finished.append(auction)
        print("User: " + auction['user'] + " has won auction:" + auction['id'] + " for " + str(auction["quantity"]) + " units for " + str(auction["top_bid"]))


    def addBuyers(self, Buyers):
        "Create and join all the buyers to all auction rooms"
        for room in self.auctions:
            for buyer in Buyers:
                if(not link.addUser(room['id'], buyer.id)):
                    print("Error adding user: " + buyer.id + " to roomID + " + room + ", aborting")
                    return False
    
    def createAuctionList(self, seller):
        "Creates a list which contains the necessary information about the auctions"
        temp = []
        topBid = 0
        for seller in self.sellers:
            if(not seller.createAuction()):
                print("Error when sending auction to API")
                return
            topBid = link.getRoomInfo(seller.auctionId, "Seller", 'bid')
            if(len(topBid) == 0):
                temp.append({'id' : seller.auctionId, 'quantity' : seller.quantity, 'user':'N/A' , 'top_bid' : 0})
            else:
                topBid = topBid[0]  
                temp.append({'id' : seller.auctionId, 'quantity' : seller.quantity, 'user':topBid ['user'] , 'top_bid' : topBid['value']})     # Should contain all the information needed per auction
        return temp
    
    def createAuctionStatus(self, auctionList):
        "Creates a list with auction ID and how many loops since latest bid"
        result = []
        for auction in auctionList:
            result.append({'id':auction['id'], 'val' : 0})                  # Default 0 meaning auction just submitted
