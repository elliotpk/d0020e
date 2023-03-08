import APILink as link
from Bidder import *
from Sellers import Sellers
import random
from DataManagement import *
import os

class SimEngine():
    def __init__(self, sellers, buyers, slot_size, threshold):
        self.end_threshold = threshold                                              # How many rounds of inactive to keep an auction running for
        self.slot_size = slot_size                                                  # How many auctions per "time slot"
        self.sellers = sellers
        self.auctions = self.createAuctionList(self.sellers)                        # Create a list of all auctions
        self.auctionStatus = self.createAuctionStatus(self.auctions)                # Used to keep track of when a bid has not been placed recently (within x loops)
        self.loopLength = len(self.auctions)
        self.auctionSlot = []                                                       # Holds all the auctions currently available to the bidders
        self.finishedAuctions = []                                                  # Auctions which have ended are placed here
        self.buyers = buyers
        self.dataManagement = DataManagement()
        self.counter = 0
        if(not self.addBuyers(self.buyers)):                                        # Error checking if adding buyers to auctions went well
            return None

    def simStart(self):
        "Start the simulation"
        #Round Start
        while(len(self.finishedAuctions) != self.loopLength):
            self.counter += 1
            if(len(self.auctionSlot) == 0):
                self.updateAuctionSlot()
                for buyer in self.buyers:
                    buyer.newRound()

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
        
        # Update the auction list with the final result, and compute resulting fairness
        for auction in self.finishedAuctions:
            info = link.getRoomInfo(auction['id'], "Seller", 'bid')[0]
            auction['top_bid'] = info['value']
            auction['user'] = info['user']
        fairness = self.fairnessCalc()
        self.saveData(fairness)
        self.dataManagement.simulationDone()

    # Starts new auctions, typically ran when the current slot is empty
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

    # Ends an auction, moves it into a new list
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
            for i in range(len(seller.auctionId)):
                topBid = link.getRoomInfo(seller.auctionId[i], "Seller", 'bid')
                if(len(topBid) == 0):
                    temp.append({'id' : seller.auctionId[i], 'quantity' : seller.quantity[i], 'user':'N/A' , 'top_bid' : 0})
                else:
                    topBid = topBid[0]  
                    temp.append({'id' : seller.auctionId[i], 'quantity' : seller.quantity[i], 'user':topBid ['user'] , 'top_bid' : topBid['value']})     # Should contain all the information needed per auction
        return temp
    
    def createAuctionStatus(self, auctionList):
        "Creates a list with auction ID and how many loops since latest bid"
        result = []
        for auction in auctionList:
            result.append({'id':auction['id'], 'val' : self.end_threshold})                  # If threshold value goes below 0 we end the auction
        return result
    
    def fairnessCalc(self):
        avgPrices = []
        for buyer in self.buyers:                                           # Calculate the average price per unit each buyer got to buy
            temp = 0                                                        # Only pays attention to buyers which have bought something
            i = 0
            for auction in self.finishedAuctions:
                if(buyer.id == auction['user']):
                    temp += auction['top_bid']/auction['quantity']
                    i += 1
            if i > 0:
                avgPrices.append(temp/i)
            else:
                continue
        nom = sum(avgPrices)**2
        denom = sum([x**2 for x in avgPrices]) * len(avgPrices)
        fairness = nom/denom
        return fairness

    # Saves the data to a csv with the won auctions and resulting fairness from it
    def saveData(self, fairness):
        output = "Fairness: {} \nRoomID, Quantity, Winner, Price \n".format(fairness)
        for auction in self.finishedAuctions:
            output += auction['id'] + ',' + str(auction['quantity']) + ',' + auction['user'] + ',' + str(auction['top_bid']) + '\n'
        num = 0
        while(os.path.exists('test'+str(num)+'.csv')):
            num += 1
        f = open('test'+str(num)+'.csv',"w")
        finalStatus = self.bidderFinalStatus()
        f.write(output + '\n' + finalStatus)
        f.close()

    # Aggregates the final result for each of the bidders such as how much they paid and how unfulfilled demand left
    def bidderFinalStatus(self):
        output = 'Behaviour, BuyerId, PricePaid, QuantityBought, DemandLeft\n'
        for buyer in self.buyers:
            bidderId = buyer.id
            bidderNeed = buyer.needs.amount
            quantityBought = 0
            pricePaid = 0
            noAuctions = 0
            for auction in self.finishedAuctions:
                if(auction['user'] == bidderId):
                    noAuctions += 1
                    quantityBought += auction['quantity']
                    pricePaid += auction['top_bid']/auction['quantity']
            if(noAuctions == 0): noAuctions = -1
            output += buyer.behaviour['behaviour'] + ', '+ bidderId + ', ' + str(pricePaid/noAuctions) + ', ' + str(quantityBought) + ', ' + str(bidderNeed - quantityBought) + '\n'
        return output
