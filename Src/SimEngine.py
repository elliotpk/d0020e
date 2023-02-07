import APILink as link

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
            return False

    def simStart(self):
        ""
        #Round Start
        for i in range(self.roundLimit):
            # Update the auction list with current values
            for auction in self.auctions:
                info = link.getRoomInfo(auction, "Seller", 'bid')[0]   # Get highest bid in the auctions, auth is 'Seller' for all auctions in the current implementation
                auction['top_bid'] = info['value']
                auction['user'] = info['user']
            
            newBids = []
            # Send updated auction list to buyers and wait for their decision
            for buyer in self.buyers:
                temp = buyer.bidUpdate(self.auctions)

            # Solve any ties in the bids/sort the list

            for bid in newBids:
                r = link.placeBid(bid['id'], bid['user'], bid['value'])
                if(not r):
                    print('Error when placing the bid for user: ' + bid['user'] + ' to auction: ' + bid['id'])

            # Call data management somewhere in the loop to save data per round basis
        
        # Update the auction list with the final result
        for auction in self.auctions:
            info = link.getRoomInfo(auction, "Seller", 'bid')[0]
            auction['top_bid'] = info['value']
            auction['user'] = info['user']
        # Decide the winners for all the auctions and save the results
        for auction in self.auctions:
            link.endAuction(auction['id'], 'Seller', auction['user'])
            # endAuction is at a very basic stage currently
            printdata(auction['top_bid'] + ',N/A,' + auction['user'] + ',' + auction['id'])
            

    def addBuyers(self, Buyers):
        "Create and join all the buyers to all auction rooms"
        names = []  # need to get the names somewhere, either predetermined or taken from bidder class. Needs to be added to the DB
        for room in self.auctions:
            for name in names:
                if(not link.addUser(room, name)):
                    print("Error adding user: " + name + " to roomID + " + room + ", aborting")
                    return False
    
    def createAuctionList(self, sellers):
        "Creates a list which contains the necessary information about the auctions"
        temp = []
        topBid = 0
        for seller in self.sellers:
            topBid = link.getRoomInfo(seller.auctionId, "Seller", 'bid')[0]
            temp.append({'id' : seller.auctionId, 'quantity' : seller.quantity, 'user':topBid ['user'] , 'top_bid' : topBid['value']})     # Should contain all the information needed per auction
        return temp
