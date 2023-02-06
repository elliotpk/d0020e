import Behaviour
import random

class Bidder:
  def __init__(self, id, amount, needs, marketPrice, behaviour):
    self.id = id
    self.initAmount = amount
    self.currentAmount = self.initAmount
    self.needs = needs
    self.marketPrice = marketPrice
    self.behaviour = behaviour

    # Bidders know this info about auctions
    self.auctionsLost = 0
    self.auctionBids = 0
    self.auctionList = []
    self.currentAuctions = len(self.auctionList)
    self.winningAuctions = 0

  # A bidder will return the lowest to bid on an auction and the auction for that bid.
  # The function loops through all the auctions to find the best auction to bid on.
  # If the bidder doesn't want to bid, it returns None, None.
  # Note: it doesn't set the current amount to a new value currently.
  def bid(self):
    # Update the aggressiveness of the behaviour
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentAuctions, self.auctionsLost, self.auctionBids)
    # Variables to keep track on the best bid for a certain auction
    bestBid = 0
    bestAuction = Auction(0,0)

    # Analyze all the auctions
    for auction in self.auctionList:
      # If a bidder only wants to bid max, it will do it in the first auction
      if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and self.behaviour["onlyBidMaxAmount"]:
        return self.currentAmount, auction
      else:
        bid = int(min(auction.price * (1 + self.behaviour["aggressiveness"] * random.uniform(0, 1)), self.currentAmount))
        
        # Print for testing purposes:
        print("<from bid(self)> bid: ",bid,"  |  bestBid: ", bestBid, "  |  auction: ", auction.auctionID)
        
        # Checks if the bidder can bid and if it wants to bid if the market price is over the generated bid.
        if self.behaviour["bid"](auction.price, self.marketPrice, self.currentAmount) and (self.marketPrice > bid and not self.behaviour["bidOverMarketPrice"]):
          if(bestBid < bid and bestBid > 0):
            continue
          else:
            bestBid = bid
            bestAuction = auction
        else:
          continue
    if(bestBid == 0 or (bestAuction.auctionID == 0 and bestAuction.price == 0)):
      return None, None
    else:
      return bestBid, bestAuction

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

class Auction:
  def __init__(self, auctionID, price):
    self.auctionID = auctionID
    self.price = price

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
    bidder1.addAuction(Auction(1, 14000))
    bidder1.addAuction(Auction(2, 13000))
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
  bidder3.addAuction(Auction(1, 14000))
  bidder3.addAuction(Auction(2, 13000))
  bidder3.addAuction(Auction(3, 11000))
  bidder3.addAuction(Auction(4, 12000))

  for auction in bidder3.auctionList:
    print("Bidder 3 participates in auction ", auction.auctionID ,"  |  auction price: ", auction.price, "  |  market price: ", bidder3.marketPrice) 
  bestBid, bestAuction = bidder3.bid()
  if(bestBid == None or bestAuction == None):
    print("Bidder 3 doesn't bid in any auction, the price is over market value.")
  else:
    print("Bidder 3 bids ", bestBid, " on auction ", bestAuction.auctionID)

  print("Testing the bid function with multiple auction strategies (Bidder 1): ")
  bidder1.addAuction(Auction(1, 14000))
  bidder1.addAuction(Auction(2, 13000))
  bidder1.addAuction(Auction(3, 11000))
  bidder1.addAuction(Auction(4, 12000))

  for auction in bidder3.auctionList:
    print("Bidder 1 participates in auction ", auction.auctionID ,"  |  auction price: ", auction.price, "  |  market price: ", bidder1.marketPrice) 
  bestBid2, bestAuction2 = bidder1.bid()
  if(bestBid2 == None or bestAuction2 == None):
    print("Bidder 1 doesn't bid in any auction.")
  else:
    print("Bidder 1 bids ", bestBid2, " on auction ", bestAuction2.auctionID)


#test()
