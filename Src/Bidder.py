import Behaviour
import random
# Matplotlib imported for testing only
import matplotlib.pyplot as plt 

###### amount should maybe be an amount taken from behaviour ######
class Bidder:
  def __init__(self, id, amount, needs, marketPrice, behaviour):
    self.id = id
    self.initAmount = amount
    self.currentAmount = self.initAmount
    self.needs = needs
    # Bidders will somewhat know the market price based on normal distribution (mean, standardDeviation)
    self.marketPrice = marketPrice*random.normalvariate(1, 0.03)
    print("<init Class Bidder> Bidder ",self.id, " knows the market price: ", self.marketPrice)
    self.behaviour = behaviour
    self.currentItems = 0
    self.marketPriceFactor = behaviour["marketPriceFactor"]

    # Bidders know this info about auctions
    self.auctionsLost = 0
    self.auctionBids = 0
    self.auctionList = []
    self.currentAuctions = len(self.auctionList)
    self.winningAuctions = 0
    self.rounds = 0

  
  # New bid function (Work In Progress)
  # Returns a list of all the auctions that the bidder can bid on
  # Note: it doesn't set the current amount to a new value currently.
  ############# self.behaviour["bidOverMarketPrice"] and a value of a range, can turn on/off if market price matters in the simulation or not ##############
  def bid(self):
    # Update the aggressiveness of the behaviour
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentAuctions, self.auctionsLost, self.auctionBids)
    # Variables to keep track on the best bid for a certain auction
    tempBid = 0
    tempAuction = Auction(0,0,0)
    allBidsList = []

    # Analyze all the auctions
    for auction in self.auctionList:
      # If a bidder only wants to bid max, it will do it in the first auction
      if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and self.behaviour["onlyBidMaxAmount"]:
        allBidsList.append((self.currentAmount, auction))
        return allBidsList
      else:
        genBid = int(min(auction.price * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor), self.currentAmount))
        
        # Print for testing purposes:
        print("<from bid2()> genBid: ", genBid, "  |  tempBid: ", tempBid, "  |  auction: ", auction.auctionId)
        
        # Checks if the bidder can bid and if it wants to bid if the market price is over the generated bid.
        if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and (self.marketPrice > genBid and not self.behaviour["bidOverMarketPrice"]):
          if(tempBid < genBid and tempBid > 0):
            continue
          else:
            tempBid = genBid
            tempAuction = auction
            allBidsList.append((tempBid, tempAuction))
        else:
          continue
    if(tempBid == 0 or (tempAuction.auctionId == 0 and tempAuction.price == 0 and tempAuction.quantity == 0)):
      return []
    else:
      return allBidsList

  def setCurrentAmount(self, amount):
    self.currentAmount = amount

  def setWinningAuctions(self, winningAuctions):
    self.winningAuctions = winningAuctions

  def setAuctionsLost(self, auctionsLost):
    self.auctionsLost = auctionsLost

  def setAuctionBids(self, auctionBids):
    self.auctionBids = auctionBids

  def addAuction(self, auction):
    self.auctionList.append(auction)
    self.currentAuctions = len(self.auctionList)

  def removeAuction(self, auctionId):
    for auction in self.auctionList:
      if(auction.auctionId == auctionId):
        self.auctionList.remove(auction)
        self.currentAuctions = len(self.auctionList)
  
  def updateMarketFactor(self, mean, standardDeviation):
    self.marketPriceFactor = self.behaviour["marketPriceFactorUpdate"](mean, standardDeviation)

  # Returns a list of dictionaries with info about how the bidder bids, work in progress
  ###### delete quantity from return                             ###### --done--
  ###### function, wins auction, need to know the Needs          ######
  ###### should be able to reset current items, winning auctions ######
  def bidUpdate(self, input):
    self.winningAuctions = 0
    for dictionary in input:
      for auction in self.auctionList:
        if(dictionary["user"] == self.id):
          self.winningAuctions =+ 1
        if(auction.auctionId == dictionary["id"]):
          auction.price = dictionary["top_bid"]
          auction.winner = dictionary["user"]
          auction.quantity = dictionary["quantity"]

    bidList = self.bid()
    print("bidList: ", bidList)
    returnList = []
    # bid[0] = bid <int>, bid[1] = auction <Auction>
    for bid in bidList:
      if(bid[1].winner == self.id):
        print("<bidUpdate()> winner")
        continue
      if(bid[0] == None or bid[1] == None):
        print("<bidUpdate()> None")
        continue
      if(self.checkWinner(bid[0], bid[1])):
        print("<bidUpdate()> append to list")
        self.winningAuctions =+ 1
        bid[1].winner = self.id
        self.currentItems = self.currentItems + bid[1].quantity
        returnList.append({'id' : bid[1].auctionId, 'user' : self.id, 'top_bid' : bid[0]})
    return returnList 
  
  # Checks if the bidder won the auction, work in progress
  def checkWinner(self, bid, auction):
    isWinner = False
    if(bid < auction.price and bid > 0):
      isWinner = False
    else:
      isWinner = True
    return isWinner

######### Auction class isn't needed maybe. ##########
class Auction:
  def __init__(self, auctionId, price, quantity):
    self.auctionId = auctionId
    self.price = price
    self.quantity = quantity
    self.winner = None
    self.round = 0

class Needs:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

# Testing method for testing different behaviours
def test():
  bidder1 = Bidder(1, 150000, Needs(55, "steel beam"), 15000, Behaviour.A)
  bidder2 = Bidder(2, 150000, Needs(55, "steel beam"), 15000, Behaviour.B)
  bidder3 = Bidder(3, 150000, Needs(55, "steel beam"), 15000, Behaviour.C)

  print("Created 3 bidders with behaviour type A, B and C respectively.")
  print("-----------------------------------------------------------------")

  print("Testing normal distribution of the marketPriceFactor() function:")
  
  print(Behaviour.B["marketPriceFactorUpdate"](1, 0.15))
  print(bidder2.behaviour["marketPriceFactorUpdate"](1, 0.15))
  print("-----------------------------------------------------------------")

  print("Testing the bid2() function and marketPriceFactor:")
  print("Creating bidder 4 (everything is the same as bidder 3, except the ID)")
  bidder4 = Bidder(4, 150000, Needs(55, "steel beam"), 15000, Behaviour.C)
  bidder4.addAuction(Auction(1, 14000, 55))
  bidder4.addAuction(Auction(2, 13000, 55))
  bidder4.addAuction(Auction(3, 11000, 55))
  bidder4.addAuction(Auction(4, 12000, 55))

  bidder3.addAuction(Auction(1, 14000, 55))
  bidder3.addAuction(Auction(2, 13000, 55))
  bidder3.addAuction(Auction(3, 11000, 55))
  bidder3.addAuction(Auction(4, 12000, 55))
  # same factor for all bidders with the same type
  #Behaviour.C["marketPriceFactorUpdate"](1, 0.15)
  # different factor for all bidders with the same type
  bidder4.updateMarketFactor(4, 2.15)
  bidder3.updateMarketFactor(4, 2.15)
  print("Market price factor bidder 3: ",bidder3.marketPriceFactor)
  print("Market price factor bidder 4: ",bidder4.marketPriceFactor)
  
  print("Bidder ",bidder3.id, " bids on auctions:")
  bidsList1 = bidder3.bid()
  if(bidsList1 == []):
    print("Bidder 3 doesn't bid in any auction.")
  else:
    for bid in bidsList1:
      print("Bidder 3 can bid ", bid[0] , " on auction ", bid[1].auctionId)

  print("Bidder ",bidder4.id, " bids on auctions:")
  bidsList2 = bidder4.bid()
  if(bidsList2 == []):
    print("Bidder 4 doesn't bid in any auction.")
  else:
    for bid in bidsList2:
      print("Bidder 4 can bid ", bid[0] , " on auction ", bid[1].auctionId)
  print("-----------------------------------------------------------------")

  print("Testing the bidUpdate() function:")
  simList = [{'id' : 1, 'quantity' : 60, 'user':None , 'top_bid' : 14000},
             {'id' : 2, 'quantity' : 55, 'user':None , 'top_bid' : 13000},
             {'id' : 3, 'quantity' : 40, 'user':None , 'top_bid' : 11000},
             {'id' : 4, 'quantity' : 50, 'user':None , 'top_bid' : 12000}]

  bidder3Info = bidder3.bidUpdate(simList)
  bidder4Info = bidder4.bidUpdate(simList)

  print("Bidder 3 decisions: ", bidder3Info)
  print("Bidder 4 decisions: ", bidder4Info)


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

