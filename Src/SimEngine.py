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


#print(Api.data) print to csv-file

class SimEngine():
    def __init__(self, sellers, roundLimit, buyers):
        self.sellers = sellers
        self.Buyers = buyers
        self.auctions = self.getAuctionIDs(self.sellers)
        self.buyers = buyers
        if(not self.addBuyers(self.buyers)):
            return False

    def simStart(self):
        ""
        #Round Start
        for auction in self.auctions:
            link.getRoomInfo(auction)


    def addBuyers(self, Buyers):
        "Create and join all the buyers to all auction rooms"
        names = []  # need to get the names somewhere...
        for room in self.auctions:
            for name in names:
                if(not link.addUser(room, name)):
                    print("Error adding user: " + name + " to roomID + " + room + ", aborting")
                    return False
    
    def getAuctionIDs(self, sellers):
        ""
        temp = []
        for seller in self.sellers:
            temp.append(seller.auctionId)
        return temp