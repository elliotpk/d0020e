import APILink as link
from Sellers import Sellers
import random
from DumbBidder import DumbBidder
#roundnumber = get from main
#actualnumber = loop

#class SimEngine

#initActuion

#run until actual=roundnumber
#Api.data
#send data to list of bidders for
#prosses bidders
#send to api
#actual++


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
    def __init__(self, sellers, roundLimit, buyers):
        self.roundLimit = roundLimit
        self.sellers = sellers
        self.Buyers = buyers
        self.auctions = self.createAuctionList(self.sellers)    # Create a list of all auctions
        self.buyers = buyers
        if(not self.addBuyers(self.buyers)):                # Error checking if adding buyers to auctions went well
            return None


    def simStart(self):
        ""
        #Round Start
        for i in range(self.roundLimit):
            # Update the auction list with current values
            for auction in self.auctions:
                info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]   # Get highest bid in the auctions, auth is 'Seller' for all auctions in the current implementation
                auction['top_bid'] = info['value']
                auction['user'] = info['user']
            
            
            # Send updated auction list to buyers and wait for their decision
            newBids = []
            for buyer in self.buyers:
                temp = buyer.update(self.auctions)
                newBids.append(temp)

            finished = []
            for auction in self.auctions:
                bids = []
                for buyers in newBids:
                    t = next((item for item in buyers if item["id"] == auction["id"]), None)                  # Extracts all the bids for each auction ID
                    if(t != None):
                        bids.append(t)
                sort = sorted(bids, key=lambda i:int(i['value']), reverse=True)                         # Sorts the list of bids by amount
                max_bid = sort[0]['value']
                for i in range(len(sort)-1, 0, -1):                                                     # Removes duplicate top bids, maybe not necessary could perhaps be done more efficiently
                    if(int(sort[i]['value']) == int(max_bid)):
                        sort.pop(i)
                print("New top bid of: "+ str(sort[0]['value']) +" submitted for auction: " + auction['id'] + " by user: " + sort[0]['user'])
                finished.append(sort)

            for id in finished:
                for bid in id:
                    r = link.placeBid(bid['id'], bid['user'], bid['value'])
                    if(not r):
                        print('Error when placing the bid for user: ' + bid['user'] + ' to auction: ' + bid['id'])
            input("-----------------------")
            # Call data management somewhere in the loop to save data per round basis
        
        # Update the auction list with the final result
        for auction in self.auctions:
            info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]
            auction['top_bid'] = info['value']
            auction['user'] = info['user']
        # Decide the winners for all the auctions and save the results
        for auction in self.auctions:
            link.endAuction(auction['id'], 'Seller', auction['user'])
            print("User: " + auction['user'] + " has won auction:" + auction['id'] + " for " + str(auction["quantity"]) + " units for " + str(auction["top_bid"]))
            # endAuction is at a very basic stage currently
            #printdata(auction['top_bid'] + ',N/A,' + auction['user'] + ',' + auction['id'])
            

    def addBuyers(self, Buyers):
        "Create and join all the buyers to all auction rooms"
        for room in self.auctions:
            for buyer in Buyers:
                if(not link.addUser(room['id'], buyer.id)):
                    print("Error adding user: " + buyer.id + " to roomID + " + room + ", aborting")
                    return False
    
    def createAuctionList(self, sellers):
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

sellerAmount = int(input('How many sellers?\n'))
limit = int(input('How many rounds?\n'))
buyerAmount = int(input('How many buyers?\n'))

sellerList = []
for i in range(sellerAmount):
    sellerList.append(Sellers('Seller'+str(i), random.randint(100, 500)))

buyerList = []
for i in range(buyerAmount):
    buyerList.append(DumbBidder('Buyer'+str(i)))

engine = SimEngine(sellerList, limit, buyerList)
engine.simStart()
