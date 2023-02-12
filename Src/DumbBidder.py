import random

BASE_BID = 20

# THIS BIDDER DOES NOT CARE ABOUT SUPPLY/DEMAND, JUST WANTS TO WIN AUCTIONS
class DumbBidder():
    def __init__(self, id):
        self.id = id
        self.auctions = []
    
    def update(self, input):
        self.auctions = []
        for auction in input:
            self.auctions.append(auction)
        
        bids = self.findBids(self.auctions)
        return bids
    
    def findBids(self, input):
        bids = []
        for auction in input:
            if(auction['user'] == self.id):     # Skip if self is the leading bid
                continue
            temp = {'id' : auction['id'], 'user' : self.id}
            if(auction['top_bid'] == 0):
                temp['value'] = BASE_BID * random.randrange(1, 10)
            else:
                temp['value'] = int(auction['top_bid']) + BASE_BID * random.randrange(1, 10)           
            bids.append(temp)
        
        return bids
            
