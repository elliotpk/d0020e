import Behaviour
import random
# Matplotlib imported for testing only
import matplotlib.pyplot as plt 

###### amount should maybe be an amount taken from behaviour ######
class Bidder:
  def __init__(self, id, needs, marketPrice, behaviour):
    self.id = id
    self.needs = needs
    # Bidders will somewhat know the market price based on normal distribution (mean, standardDeviation)
    self.marketPrice = marketPrice*random.normalvariate(1, 0.03)
    self.behaviour = behaviour
    self.marketPriceFactor = behaviour["marketPriceFactor"]
    # Stops the bidders from bidding over a certain value based on market price and aggressiveness (code is also added in Behaviour.py)
    self.stopBid = self.marketPrice*(1 + self.behaviour["aggressiveness"])
    #print("<init Class Bidder> Bidder ",self.id, " knows the market price: ", self.marketPrice, " and stopBid is: ", self.stopBid)

    # Bidders know this info about auctions
    self.auctionsLost = 0 # not used
    self.auctionBids = 0 # not used
    self.currentAuctions = 0 # not used, is currently len(input) in bid(self, input) used by bidUpdate(self, input)
    self.winningAuctions = 0 # is only incrementing in bidUpdate(), but isn't used anywhere
    self.wonItems = 0
    self.rounds = 0 # not used

  
  # New bid function (Work In Progress)
  # Returns a list of all the auctions that the bidder can bid on
  # Note: it doesn't set the current amount to a new value currently.
  ############# self.behaviour["bidOverMarketPrice"] and a value of a range, can turn on/off if market price matters in the simulation or not ##############
  def bid(self, input):
    # Update the aggressiveness of the behaviour (doesn't get new values for auctionsLost or auctionBids currently)
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](len(input), self.auctionsLost, self.auctionBids)
    # Variables to keep track on the best bid for a certain auction
    tempBid = 0
    tempAuction = {}
    allBidsList = []

    for auction in input:
      genBid = int(auction["top_bid"] * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))
      
      # If top bid starts with 0, then the bidders will bid 1/5 of the market price or what is left in their current amount.
      if(genBid == 0):
        genBid = int((self.marketPrice/5) * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))

      # Print for testing purposes:
      #print("<from bid()> Bidder",self.id, "genBid: ", genBid, "  |  tempBid: ", tempBid, "  |  stopBid: ",self.behaviour["stopBid"](self.marketPrice), "  |  auction: ", auction["id"])
      
      # Checks if the bidder can bid and if it wants to bid if the market price is over the generated bid.
      if(((self.marketPrice > genBid and not self.behaviour["bidOverMarketPrice"]) or (self.stopBid > genBid and self.behaviour["bidOverMarketPrice"]))
          or
          self.behaviour["bidOverMarketPrice"]
      ):
        # Bidders won't bid if the top bid is over the stop bid
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
    if(tempBid < 0 or (tempAuction["id"] == 0 and tempAuction["top_bid"] == 0 and tempAuction["quantity"] == 0)):
      return []
    else:
      return allBidsList
  
  def updateMarketFactor(self, mean, standardDeviation):
    self.marketPriceFactor = self.behaviour["marketPriceFactorUpdate"](mean, standardDeviation)
  
  def updateWonItems(self, wonItems):
    self.wonItems += wonItems

  # Returns a list of dictionaries with info about how the bidder bids
  # Note: currently it can bid on many auctions even if it just needs a small amount to fulfill the needs
  ###### function, wins auction, need to know the Needs          ###### --Maybe works now?--
  ###### should be able to reset current items, winning auctions ###### --Maybe works now?--
  def bidUpdate(self, input):
    self.winningAuctions = 0
    satisfiedNeed = 0
    currentItems = 0

    for dictionary in input:
      if(dictionary["user"] == self.id):
          self.winningAuctions =+ 1
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

    return returnList 

class Needs:
  def __init__(self, amount, type):
    self.amount = amount
    self.type = type

# Testing method for testing different behaviours
def test():
  bidder1 = Bidder('1', Needs(55, "steel beam"), 15000, Behaviour.A)
  bidder2 = Bidder('2', Needs(55, "steel beam"), 15000, Behaviour.B)
  bidder3 = Bidder('3', Needs(55, "steel beam"), 15000, Behaviour.C)
  bidder4 = Bidder('4', Needs(55, "steel beam"), 15000, Behaviour.C)

  print("Created 3 bidders with behaviour type A, B and C respectively and an extra bidder with type C.")
  print("-----------------------------------------------------------------")

  print("Testing the bidUpdate() function:")
  simList = [{'id' : '1', 'quantity' : 60, 'user':'N/A' , 'top_bid' : 16000},
             {'id' : '2', 'quantity' : 55, 'user':'N/A' , 'top_bid' : 13000},
             {'id' : '3', 'quantity' : 40, 'user':'N/A' , 'top_bid' : 11000},
             {'id' : '4', 'quantity' : 50, 'user':'N/A' , 'top_bid' : 12000}]
  simList2 = [{'id': '63f6c3df7b6103af971aba61', 'quantity': 441, 'user': 'N/A', 'top_bid': 16000},
              {'id': '63f6c3e07b6103af971aba63', 'quantity': 411, 'user': 'N/A', 'top_bid': 0}]

  bidder1.updateMarketFactor(4, 2.15)
  bidder3.updateMarketFactor(4, 2.15)
  bidder4.updateMarketFactor(4, 2.15)

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


def testNormalDistributionGraph():
  print("Normal distribution test (graph):")
  value = 0
  valueList = []
  for i in range(2000):
    value = random.normalvariate(1, 0.15)
    valueList.append(value)
  plt.hist(valueList, bins=200) 
  plt.show()


#test()
#testNormalDistributionGraph()

