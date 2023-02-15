import Behaviour
import random
# Matplotlib imported for testing only
import matplotlib.pyplot as plt 


class Bidder:
  def __init__(self, id, amount, needs, marketPrice, behaviour):
    self.id = id
    self.initAmount = amount
    self.currentAmount = self.initAmount
    self.needs = needs
    self.marketPrice = marketPrice
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

  # A bidder will return the lowest to bid on an auction and the auction for that bid.
  # The function loops through all the auctions to find the best auction to bid on.
  # If the bidder doesn't want to bid, it returns None, None.
  # Note: it doesn't set the current amount to a new value currently.
  def bid(self):
    # Update the aggressiveness of the behaviour
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentAuctions, self.auctionsLost, self.auctionBids)
    # Variables to keep track on the best bid for a certain auction
    bestBid = 0
    bestAuction = Auction(0,0,0)

    # Analyze all the auctions
    for auction in self.auctionList:
      # If a bidder only wants to bid max, it will do it in the first auction
      if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and self.behaviour["onlyBidMaxAmount"]:
        return self.currentAmount, auction
      else:
        bid = int(min(auction.price * (1 + self.behaviour["aggressiveness"] * random.uniform(0.4, 0.6)), self.currentAmount))
        
        # Print for testing purposes:
        print("<from bid()> bid: ", bid, "  |  bestBid: ", bestBid, "  |  auction: ", auction.auctionID)
        
        # Checks if the bidder can bid and if it wants to bid if the market price is over the generated bid.
        if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and (self.marketPrice > bid and not self.behaviour["bidOverMarketPrice"]):
          if(bestBid < bid and bestBid > 0):
            continue
          else:
            bestBid = bid
            bestAuction = auction
        else:
          continue
    if(bestBid == 0 or (bestAuction.auctionID == 0 and bestAuction.price == 0 and bestAuction.quantity == 0)):
      return None, None
    else:
      return bestBid, bestAuction
  
  # New bid function (Work In Progress)
  # Returns a list of all the auctions that the bidder can bid on
  ########### need to update variable names ##########
  def bid2(self):
    # Update the aggressiveness of the behaviour
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentAuctions, self.auctionsLost, self.auctionBids)
    # Variables to keep track on the best bid for a certain auction
    bestBid = 0
    bestAuction = Auction(0,0,0)
    allBidsList = []

    # Analyze all the auctions
    for auction in self.auctionList:
      # If a bidder only wants to bid max, it will do it in the first auction
      if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and self.behaviour["onlyBidMaxAmount"]:
        allBidsList.append((self.currentAmount, auction))
        return allBidsList
      else:
        bid = int(min(auction.price * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor), self.currentAmount))
        
        # Print for testing purposes:
        print("<from bid2()> bid: ", bid, "  |  bestBid: ", bestBid, "  |  auction: ", auction.auctionID)
        
        # Checks if the bidder can bid and if it wants to bid if the market price is over the generated bid.
        if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and (self.marketPrice > bid and not self.behaviour["bidOverMarketPrice"]):
          if(bestBid < bid and bestBid > 0):
            continue
          else:
            bestBid = bid
            bestAuction = auction
            allBidsList.append((bestBid, bestAuction))
        else:
          continue
    if(bestBid == 0 or (bestAuction.auctionID == 0 and bestAuction.price == 0 and bestAuction.quantity == 0)):
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

  def removeAuction(self, auctionID):
    for auction in self.auctionList:
      if(auction.auctionID == auctionID):
        self.auctionList.remove(auction)
        self.currentAuctions = len(self.auctionList)
  
  def bidUpdate(self, input):
    self.winningAuctions = 0
    for dictionary in input:
      for auction in self.auctionList:
        if(dictionary["user"] == self.id):
          self.winningAuctions =+ 1
        if(auction.auctionID == dictionary["room_id"]):
          auction.price = dictionary["value"]
          auction.winner = dictionary["user"]

    bestBid, bestAuction = self.bid()
    if(bestAuction.winner == self.id):
      return None
    if(bestBid == None or bestAuction == None):
      return None
    else:
      self.winningAuctions =+ 1
      return {'id' : bestAuction.auctionID, 'user' : self.id, 'top_bid' : bestBid}
    

class Auction:
  def __init__(self, auctionID, price, quantity):
    self.auctionID = auctionID
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

  # Bidder 1 participates in 2 auctions:
  # Bidder 1 will bid the max amount in one of the auctions because of desperate behaviour.
  # Bidder 1 can bid because the price is lower than the maximum amount that the bidder have.
  print("-----------------------------------------------------------------")
  print("Test if Bidder 1 bids the max amount in 1 of 2 auctions:")
  if(bidder1.behaviour["onlyBidMaxAmount"] == True
     and
     bidder1.behaviour["bid"](14000, bidder1.marketPrice, bidder1.currentAmount)
    ):
    print("Current auctions Bidder 1 (before participating): ",bidder1.currentAuctions)
    bidder1.addAuction(Auction(1, 14000, 55))
    bidder1.addAuction(Auction(2, 13000, 55))
    print("Bidder 1 enters 2 auctions: ", bidder1.auctionList,", current auctions: ",bidder1.currentAuctions)
    bidder1.setWinningAuctions(1)
    bidder1.setCurrentAmount(0)
    print("Bidder", bidder1.id, "bid the max amount in 1 auction.")
  else:
    print("Bidder ",bidder1.id," didn't bid in any auction.")
  # Restore the initial amount and removes the 2 auctions.
  bidder1.setCurrentAmount(bidder1.initAmount)
  bidder1.removeAuction(1)
  bidder1.removeAuction(2)
  print("Bidder 1 leaves 2 auctions: ", bidder1.auctionList,", current auctions: ",bidder1.currentAuctions)
  print("-----------------------------------------------------------------")
  
  # Tests that can make a bidder bid differently based on what a bidder knows
  # about price, market price (15000) and the maximum amount.
  print("Bid behaviour test if Bidder 1 can bid or not:")
  # Can bid (TRUE) with behaviour type A:
  print("bidMax > price > marketPrice: ", bidder1.behaviour["bid"](15001, bidder1.marketPrice, bidder1.currentAmount))
  print("bidMax > marketPrice > price: ", bidder1.behaviour["bid"](14001, bidder1.marketPrice, bidder1.currentAmount))
  print("marketPrice > bidMax > price: ", bidder1.behaviour["bid"](14001, bidder1.marketPrice, 14002))
  # Can't bid (FALSE) with behaviour type A:
  print("marketPrice > price > bidMax: ", bidder1.behaviour["bid"](14001, bidder1.marketPrice, 10000))
  print("price > marketPrice > bidMax: ", bidder1.behaviour["bid"](15001, bidder1.marketPrice, 10000))
  print("price > bidMax > marketPrice: ", bidder1.behaviour["bid"](15002, bidder1.marketPrice, 15000))
  print("-----------------------------------------------------------------")

  print("Random behaviour selection test:")
  print("1 random behaviour selection: ", Behaviour.randomBehaviour())
  # 5 times larger chance to select behaviour B
  print("1 advanced random behaviour selection: ", Behaviour.randomBehaviourAdvanced([1,5,1], 1))
  print("-----------------------------------------------------------------")

  print("Tests if Bidder 3 changes the aggressiveness in a scenario of participating in 3 auctions, 2 auctions lost and 1 current bid:")
  print("Bidder 3: initial aggressiveness: ", bidder3.behaviour["aggressiveness"])
  print("Bidder 3: changes aggressiveness: ", bidder3.behaviour["adaptiveAggressiveness"](3, 2, 1))
  print("Bidder 3: new aggressiveness: ", bidder3.behaviour["aggressiveness"])
  print("-----------------------------------------------------------------")

  print("Testing the bid function with multiple auction strategies (Bidder 3): ")
  bidder3.addAuction(Auction(1, 14000, 55))
  bidder3.addAuction(Auction(2, 13000, 55))
  bidder3.addAuction(Auction(3, 11000, 55))
  bidder3.addAuction(Auction(4, 12000, 55))

  for auction in bidder3.auctionList:
    print("Bidder 3 participates in auction ", auction.auctionID ,"  |  auction price: ", auction.price, "  |  auction quantity: ", auction.quantity) 
  bestBid, bestAuction = bidder3.bid()
  if(bestBid == None or bestAuction == None):
    print("Bidder 3 doesn't bid in any auction, the price is over market value.")
  else:
    print("Bidder 3 bids ", bestBid, " on auction ", bestAuction.auctionID)

  print("Testing the bid function with multiple auction strategies (Bidder 1): ")
  bidder1.addAuction(Auction(1, 14000, 55))
  bidder1.addAuction(Auction(2, 13000, 55))
  bidder1.addAuction(Auction(3, 11000, 55))
  bidder1.addAuction(Auction(4, 12000, 55))

  for auction in bidder1.auctionList:
    print("Bidder 1 participates in auction ", auction.auctionID ,"  |  auction price: ", auction.price, "  |  auction quantity: ", auction.quantity) 
  bestBid2, bestAuction2 = bidder1.bid()
  if(bestBid2 == None or bestAuction2 == None):
    print("Bidder 1 doesn't bid in any auction.")
  else:
    print("Bidder 1 bids ", bestBid2, " on auction ", bestAuction2.auctionID)
  print("-----------------------------------------------------------------")

  print("Testing normal distribution of the marketPriceFactor() function:")
  
  print(Behaviour.B["marketPriceFactorUpdate"](1, 0.15))
  print(bidder2.behaviour["marketPriceFactorUpdate"](1, 0.15))
  print("-----------------------------------------------------------------")

  print("Testing the bid2() function:")
  print("Creating bidder 4 (everything is the same as bidder 3, except the ID)")
  bidder4 = Bidder(4, 150000, Needs(55, "steel beam"), 15000, Behaviour.C)
  bidder4.addAuction(Auction(1, 14000, 55))
  bidder4.addAuction(Auction(2, 13000, 55))
  bidder4.addAuction(Auction(3, 11000, 55))
  bidder4.addAuction(Auction(4, 12000, 55))
  
  #Behaviour.C["marketPriceFactorUpdate"](1, 0.15)
  bidder4.marketPriceFactor = bidder4.behaviour["marketPriceFactorUpdate"](1, 0.5)
  bidder3.marketPriceFactor = bidder3.behaviour["marketPriceFactorUpdate"](1, 0.5)
  print("Market price factor bidder 3: ",bidder3.marketPriceFactor)
  print("Market price factor bidder 4: ",bidder4.marketPriceFactor)
  
  print("Bidder ",bidder3.id, " bids on auctions:")
  bidsList1 = bidder3.bid2()
  if(bidsList1 == []):
    print("Bidder 3 doesn't bid in any auction.")
  else:
    for bid in bidsList1:
      print("Bidder 3 can bid ", bid[0] , " on auction ", bid[1].auctionID)

  print("Bidder ",bidder4.id, " bids on auctions:")
  bidsList2 = bidder4.bid2()
  if(bidsList2 == []):
    print("Bidder 4 doesn't bid in any auction.")
  else:
    for bid in bidsList2:
      print("Bidder 4 can bid ", bid[0] , " on auction ", bid[1].auctionID)


def testNormalDistributionGraph():
  print("Normal distribution test (graph):")
  value = 0
  valueList = []
  for i in range(2000):
    value = random.normalvariate(1, 0.15)
    valueList.append(value)
  plt.hist(valueList, bins=200) 
  plt.show()

test()
#testNormalDistributionGraph()

