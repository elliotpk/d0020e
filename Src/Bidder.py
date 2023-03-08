import Behaviour
import random

# Bidders have an ID, needs with an amount and type.
# A bidder knows when the last round will occur.
# Every bidder has a behaviour/strategy.
class Bidder:
  def __init__(self, id, needs, maxRound, behaviour):
    self.id = id
    self.needs = needs
    self.maxRound = maxRound
    self.behaviour = behaviour
    self.marketPrice = 0
    self.stopBid = 0
    self.marketPriceFactor = self.behaviour["marketPriceFactor"]
    self.wonItems = 0
    self.currentRound = 0 

  # Bidders will somewhat know the market price per unit based on normal distribution (mean, standardDeviation).
  # Then they will stop to bid at a certain value based on the market price and their aggressiveness,
  # which will also be the maximum bid (stopBid is also per unit).
  def setMarketprice(self,price):
    self.marketPrice=price*random.normalvariate(1, 0.03)
    self.stopBid=self.marketPrice*(1 + self.behaviour["aggressiveness"])
  
  # Returns a list of all the auctions that the bidder can bid on.
  def bid(self, input):
    # Update the aggressiveness of the behaviour based on the current auction information.
    self.behaviour["aggressiveness"] = self.behaviour["adaptiveAggressiveness"](self.currentRound, self.maxRound)
    self.updateMarketFactor(1, 0.05)
    # Keeps track on auctions that the bidder wants to bid on that will be added to the list of all the bids that the bidder wants to and can bid on.
    tempBid = 0
    tempAuction = {}
    allBidsList = []

    for auction in input:
      genBid = int(auction["top_bid"] * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))
      
      # If top bid starts with 0, then the bidders will bid 1/5 of the market price multiplied by the aggressiveness and market price factor.
      if(genBid == 0):
        genBid = int((self.marketPrice*auction["quantity"]/5) * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))

      # Checks if the bidder can bid based on its behaviour about bidding over the market price.
      if(((self.marketPrice*auction["quantity"] > genBid and not self.behaviour["bidOverMarketPrice"]) or (self.stopBid*auction["quantity"] > genBid and self.behaviour["bidOverMarketPrice"]))
          or
          self.behaviour["bidOverMarketPrice"]
      ):
        if(auction["top_bid"] > self.stopBid*auction["quantity"]):
          continue
        # Limits the maximum bid to be stop bid
        if(self.stopBid*auction["quantity"] < genBid):
          tempBid = int(self.stopBid*auction["quantity"])
        else:
          tempBid = genBid
        tempAuction = auction
        allBidsList.append((tempBid, tempAuction))
      else:
        continue
    # The bidder won't bid if there is no auctions as input.
    if len(tempAuction) != 0:
      # The bidder won't bid if the auction doesn't have any quantity and a top bid that is 0 or if the bid is negative (should never happen).
      if(tempBid < 0 or (tempAuction["top_bid"] == 0 and tempAuction["quantity"] == 0)):
        return []
      else:
        return allBidsList
    else:
      return []

  # Market factor changes how different the amount will be when bidders wants to bid, it uses a mean and standard deviation value.
  def updateMarketFactor(self, mean, standardDeviation):
    self.marketPriceFactor = self.behaviour["marketPriceFactorUpdate"](mean, standardDeviation)
  
  def updateWonItems(self, wonItems):
    self.wonItems += wonItems
  
  def newRound(self):
    self.currentRound += 1

  # This function receives a list of dictionaries describing the auction states from SimEngine.
  # Returns a list of dictionaries with info about how the bidder bids.
  def bidUpdate(self, input):
    satisfiedNeed = 0
    currentItems = 0
    returnList = [] # doesn't include quantity
    tempQuantity = 0
    bidOverOnce = False
    checkOnce = True
    index = 0

    # Randomizes the input so that bidders will bid independent of the input order.
    random.shuffle(input)

    # Counts how many items that the bidder is currently winning
    for dictionary in input:
      if(dictionary["user"] == self.id):
          satisfiedNeed = satisfiedNeed + dictionary["quantity"]

    currentItems = self.needs.amount - satisfiedNeed - self.wonItems
    bidList = self.bid(input)
    
    # Doesn't bid if it the bidder is winning on items that satisfies the needs.
    # Also, the bidder shouldn't bid for more than needed on the quantity in the current round.
    # bid[0] = bid <int>, bid[1] = auction <dictionary>
    for bid in bidList:
      tempQuantity += bid[1]["quantity"]
      if(index+1 > len(bidList)-1):
        if(bid[1]["user"] == self.id):
          continue
        elif(0 < currentItems and bidOverOnce or 0 < currentItems - tempQuantity + bidList[index][1]["quantity"]):
          returnList.append({'id' : bid[1]["id"], 'user' : self.id, 'top_bid' : bid[0]})
      else:
        if(0 > currentItems - tempQuantity and checkOnce):
          bidOverOnce = True
          checkOnce = False
        if(bid[1]["user"] == self.id):
          continue
        elif(0 < currentItems and bidOverOnce or 0 < currentItems - tempQuantity + bidList[index+1][1]["quantity"]):
          returnList.append({'id' : bid[1]["id"], 'user' : self.id, 'top_bid' : bid[0]})
          bidOverOnce = False
      index += 1

    # Check if the bidder should bid based on the desperation.
    # If the current round is the last round, then the bidder must place a bid if the needs isn't satisfied.
    # Checks so that if there is an auction with no bids and if the bidder hasn't satisfied the needs,
    # it will place a last bid on that auction to satisfy the needs.
    if(self.behaviour["desperation"](self.currentRound, self.maxRound) == 0  and 0 < currentItems):
      for dictionary in input:
        # lastBid is the same as genBid from the bid(self, input) function currently.
        lastBid = int((self.marketPrice*dictionary["quantity"]/5) * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))
        noDuplicateBidOnEmptyAuction = True
        if((dictionary["user"] == "N/A" or dictionary["top_bid"] == 0) and 0 < currentItems):
            for bid in returnList:
              # Doesn't bid if the bidder already bids on the auction
              if(dictionary["id"] == bid["id"]):
                noDuplicateBidOnEmptyAuction = False
                break
              else:
                continue
            if(noDuplicateBidOnEmptyAuction):
              returnList.append({'id' : dictionary["id"], 'user' : self.id, 'top_bid' : lastBid})
      return returnList
    # If the desperation is high, then the bidder will most likely try to bid.
    if(self.behaviour["desperation"](self.currentRound, self.maxRound) >= random.random() and 0 < currentItems):
      return returnList

    return []

class Needs:
  def __init__(self, amount, type):
    self.amount = amount
    self.type = type

