import APILink as link
from Bidder import *
from Sellers import Sellers
import random
from DataManagement import *

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
    def __init__(self, sellers, buyers, slot_size, threshold):
        self.end_threshold = threshold                                              # How many rounds of inactive to keep an auction running for
        self.slot_size = slot_size                                                  # How many auctions per "time slot"
        self.sellers = sellers
        self.auctions = self.createAuctionList(self.sellers)                        # Create a list of all auctions
        self.auctionStatus = self.createAuctionStatus(self.auctions)                # Used to keep track of when a bid has not been placed recently (within x loops)
        self.loopLenght = len(self.auctions)
        self.auctionSlot = []                                                       # Holds all the auctions currently available to the bidders
        self.finishedAuctions = []                                                  # Auctions which have ended are placed here
        self.buyers = buyers
        self.dataManagement = DataManagement()
        if(not self.addBuyers(self.buyers)):                                        # Error checking if adding buyers to auctions went well
            return None

    def simStart(self):
        "Start the simulation"
        #Round Start
        while(len(self.finishedAuctions) != self.loopLenght):
            if(len(self.auctionSlot) == 0):
                self.updateAuctionSlot()
            # Update the auction list with current values
            for auction in self.auctionSlot:
                info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]   # Get highest bid in the auctions, auth is 'Seller' for all auctions in the current implementation
                auction['top_bid'] = info['value']
                auction['user'] = info['user']
                  
            # Send updated auction list to buyers and wait for their decision
            newBids = []
            for buyer in self.buyers:
                temp = buyer.bidUpdate(self.auctionSlot)
                if (len(temp) == 0):
                    continue
                newBids.append(temp)
            if(len(newBids) == 0):
                self.updateStatus([])
                continue

            finished = []
            for auction in self.auctionSlot:
                bids = []
                for buyers in newBids:
                    t = next((item for item in buyers if item["id"] == auction["id"]), None)                  # Extracts all the bids for each auction ID
                    if(t != None):
                        bids.append(t)
                sort = sorted(bids, key=lambda i:int(i['top_bid']), reverse=True)                               # Sorts the list of bids by amount
                if (len(sort) == 0): continue
                self.dataManagement.stringMaker(sort)
                # !! Pass the list "sort" to the datamanagement class here, before we pick out the top bids only !!
                max_bid = sort[0]['top_bid']
                top = []
                for i in range(len(sort)-1, -1, -1):                                                             # Pick out any potential ties for the top bid to randomize which one gets submitted
                    if(int(sort[i]['top_bid']) == int(max_bid)):
                        top.append(sort.pop(i))
                if(len(top) == 0 and len(sort) == 1):
                    finished.append(sort[0])
                else:
                    finished.append(random.choice(top))                                                           # random.choice selects a random auction from the list

            for bid in finished:
                r = link.placeBid(bid['id'], bid['user'], bid['top_bid'])
                if(not r):
                    print('Error when placing the bid for user: ' + bid['user'] + ' to auction: ' + bid['id'])
            
            self.updateStatus(finished)
        
        # Update the auction list with the final result, might not be needed really
        for auction in self.finishedAuctions:
            info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]
            auction['top_bid'] = info['value']
            auction['user'] = info['user']
        self.saveData()
        self.dataManagement.simulationDone()

    def updateAuctionSlot(self):
        for i in range(self.slot_size):
            if(len(self.auctions) == 0):
                break
            item = random.choice(self.auctions)
            i = self.auctions.index(item)
            self.auctionSlot.append(self.auctions.pop(i))

    def updateStatus(self, auctions):
        auctionIDs = [d.get('id') for d in auctions]                                                        # Find all the auction IDs present in the list "auctions"
        iter = (item for item in self.auctionSlot if auctionIDs.count(item['id']) == 0)                     # Find all the auction objects in auctionStatus which were NOT updated with a new bid
        while(True):
            item = next(iter, None)
            if(item == None):                                                                               # End the while loop when iterator has nothing more left
                break
            for auction in self.auctionStatus:
                if(auction['id'] == item['id']):
                    if(auction['val'] == 0):                                                                # If the max round duration is exceeded we end the auction
                        for slotAuction in self.auctionSlot:
                            if(slotAuction['id'] == auction['id']):
                                i = self.auctionSlot.index(slotAuction)
                                end = self.auctionSlot.pop(i)                                               # Remove the entry from the auctionstatus list and end the auction                                                          
                                self.endAuction(end)                                                                        
                    else:                                                                                   # Otherwise we decrement the max round duration counter
                        auction['val'] -= 1
                        break


    def endAuction(self, auction):
        "Called to end the specific auction"
        link.endAuction(auction['id'], 'Seller', auction['user'])
        for bidder in self.buyers:
            if bidder.id == auction["user"]:
                bidder.updateWonItems(auction["quantity"])
                break
        self.finishedAuctions.append(auction)
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
            result.append({'id':auction['id'], 'val' : self.end_threshold})                  # If threshold value goes below 0 we end the auction
        return result

    def saveData(self):
        output = "RoomID, Quantity, Winner, Price \n"
        for auction in self.finishedAuctions:
            output += auction['id'] + ',' + str(auction['quantity']) + ',' + auction['user'] + ',' + str(auction['top_bid']) + '\n'
        num = 0
        while(os.path.exists('test'+str(num)+'.csv')):
            num += 1
        f = open('test'+str(num)+'.csv',"w")
        f.write(output)
        f.close()
