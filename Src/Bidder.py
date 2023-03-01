import Behaviour
import random

###### TODO add timeslot parameter to use with behaviour ######
###### TODO rounds increase in bidUpdate, add to behaviour (exponential behaviour depending on aggressiveness and rounds) ######
###### TODO change so that marketPriceFactor changes internally in Bidder ######
class Bidder:
  def __init__(self, id, needs, timeSlot, behaviour):
    self.id = id
    self.needs = needs
    self.timeSlot = timeSlot
    self.behaviour = behaviour
    self.marketPrice = 0
    self.stopBid = 0
    # Market factor changes how different the amount will be when bidders wants to bid with a mean and standard deviation value.
    self.updateMarketFactor(1, 0.05)
    self.marketPriceFactor = self.behaviour["marketPriceFactor"]
    # Print for testing purposes:
    #print("marketPriceFactor for bidder", self.id, " is:", self.behaviour["marketPriceFactor"])
    
    # Bidders know this info about auctions
    self.auctionsLost = 0 # not used
    self.auctionBids = 0
    self.currentAuctions = 0
    self.wonAuctions = 0
    self.wonItems = 0
    self.rounds = 0 # increments in bidUpdate(), should also add to behaviour

  # Bidders will somewhat know the market price based on normal distribution (mean, standardDeviation).
  # Then they will stop to bid at a certain value based on the market price and their aggressiveness,
  # which will also be the maximum bid.
  def setMarketprice(self,price):
    self.marketPrice=price*random.normalvariate(1, 0.03)
    self.stopBid=self.marketPrice*(1 + self.behaviour["aggressiveness"])
    #print("<setMarketPrice()> Bidder ",self.id, " knows the market price: ", self.marketPrice, " and stopBid is: ", self.stopBid)
  
  # Returns a list of all the auctions that the bidder can bid on.
  ############# self.behaviour["bidOverMarketPrice"] and a value of a range, can turn on/off if market price matters in the simulation or not ##############
  def bid(self, input):
    self.currentAuctions = len(input)
    # Update the aggressiveness of the behaviour.
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentAuctions, self.auctionsLost, self.auctionBids)
    # Keeps track on auctions that the bidder wants to bid on that will be added to the list of all the bids that the bidder wants to and can bid on.
    tempBid = 0
    tempAuction = {}
    allBidsList = []

    for auction in input:
      genBid = int(auction["top_bid"] * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))
      
      # If top bid starts with 0, then the bidders will bid 1/5 of the market price multiplied by the aggressiveness and market price factor.
      if(genBid == 0):
        genBid = int((self.marketPrice/5) * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))

      # Print for testing purposes:
      #print("<from bid()> Bidder",self.id, "genBid: ", genBid, "  |  tempBid: ", tempBid, "  |  stopBid: ",self.behaviour["stopBid"](self.marketPrice), "  |  auction: ", auction["id"])
      
      # Checks if the bidder can bid based on its behaviour about bidding over the market price.
      if(((self.marketPrice > genBid and not self.behaviour["bidOverMarketPrice"]) or (self.stopBid > genBid and self.behaviour["bidOverMarketPrice"]))
          or
          self.behaviour["bidOverMarketPrice"]
      ):
        if(auction["top_bid"] > self.stopBid):
          continue
        # Limits the maximum bid to be stop bid
        if(self.stopBid < genBid):
          tempBid = int(self.stopBid)
        else:
          tempBid = genBid
        tempAuction = auction
        allBidsList.append((tempBid, tempAuction))
      else:
        continue
    # The bidder won't bid if there is no auctions as input.
    if len(tempAuction) != 0:
      # The bidder won't bid if the auction doesn't have any quantity and a top bid that is 0 or if the bid is negative.
      if(tempBid < 0 or (tempAuction["top_bid"] == 0 and tempAuction["quantity"] == 0)):
        return []
      else:
        return allBidsList
    else:
      return []

  def updateMarketFactor(self, mean, standardDeviation):
    self.marketPriceFactor = self.behaviour["marketPriceFactorUpdate"](mean, standardDeviation)
  
  def updateWonItems(self, wonItems):
    self.wonItems += wonItems
    self.wonAuctions += 1

  def lostAuction(self):
    self.auctionsLost += 1

  # Returns a list of dictionaries with info about how the bidder bids
  # Note: currently it can bid on many auctions even if it just needs a small amount to fulfill the needs
  def bidUpdate(self, input):
    satisfiedNeed = 0
    currentItems = 0
    self.rounds += 1

    for dictionary in input:
      if(dictionary["user"] == self.id):
          satisfiedNeed = satisfiedNeed + dictionary["quantity"]

    currentItems = self.needs.amount - satisfiedNeed - self.wonItems
    bidList = self.bid(input)
    returnList = []

    # bid[0] = bid <int>, bid[1] = auction <dictionary>
    for bid in bidList:
      if(bid[1]["user"] == self.id):
        continue
      elif(0 < currentItems):
        returnList.append({'id' : bid[1]["id"], 'user' : self.id, 'top_bid' : bid[0]})
        self.auctionBids += 1

    return returnList 

class Needs:
  def __init__(self, amount, type):
    self.amount = amount
    self.type = type

# Testing method for testing different behaviours
def test():
  bidder1 = Bidder('1', Needs(55, "steel beam"), 0, Behaviour.A)
  bidder2 = Bidder('2', Needs(55, "steel beam"), 0, Behaviour.B)
  bidder3 = Bidder('3', Needs(55, "steel beam"), 0, Behaviour.C)
  bidder4 = Bidder('4', Needs(55, "steel beam"), 0, Behaviour.C)

  print("Created 3 bidders with behaviour type A, B and C respectively and an extra bidder with type C.")
  print("-----------------------------------------------------------------")

  print("Testing the bidUpdate() function:")
  simList = [{'id' : '1', 'quantity' : 60, 'user':'N/A' , 'top_bid' : 16000},
             {'id' : '2', 'quantity' : 55, 'user':'N/A' , 'top_bid' : 13000},
             {'id' : '3', 'quantity' : 40, 'user':'N/A' , 'top_bid' : 11000},
             {'id' : '4', 'quantity' : 50, 'user':'N/A' , 'top_bid' : 12000}]
  simList2 = [{'id': '63f6c3df7b6103af971aba61', 'quantity': 441, 'user': 'N/A', 'top_bid': 16000},
              {'id': '63f6c3e07b6103af971aba63', 'quantity': 411, 'user': 'N/A', 'top_bid': 0}]

  bidder1.setMarketprice(15000)
  bidder3.setMarketprice(15000)
  bidder4.setMarketprice(15000)

  bidder1Info = bidder1.bidUpdate(simList2)
  bidder3Info = bidder3.bidUpdate(simList2)
  bidder4Info = bidder4.bidUpdate(simList2)

  print("Bidder 1 decisions: ", bidder1Info)
  #print("Bidder 1 needs: ", bidder1.needs.amount)
  #print("Bidder 1 stopBid: ", bidder1.behaviour["stopBid"](bidder1.marketPrice))
  print("Bidder 3 decisions: ", bidder3Info)
  #print("Bidder 3 needs: ", bidder3.needs.amount)
  #print("Bidder 3 stopBid: ", bidder3.behaviour["stopBid"](bidder3.marketPrice))
  print("Bidder 4 decisions: ", bidder4Info)
  #print("Bidder 4 needs: ", bidder4.needs.amount)
  #print("Bidder 4 stopBid: ", bidder4.behaviour["stopBid"](bidder4.marketPrice))


#test()

