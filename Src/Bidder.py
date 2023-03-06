import Behaviour
import random

# Bidders have an ID, needs with an amount and type.
# A bidder knows when the last round will occur.
# Every bidder has a behaviour/strategy.
###### TODO add a check so that bidders doesn't bid for more quanitity than needed ######
class Bidder:
  def __init__(self, id, needs, maxRound, behaviour):
    self.id = id
    self.needs = needs
    self.maxRound = maxRound
    self.behaviour = behaviour
    self.marketPrice = 0
    self.stopBid = 0
    # Market factor changes how different the amount will be when bidders wants to bid with a mean and standard deviation value.
    self.updateMarketFactor(1, 0.05)
    self.marketPriceFactor = self.behaviour["marketPriceFactor"]
    
    # Bidders know this info about auctions
    self.auctionsLost = 0 # not used, maybe shouldn't be needed
    self.auctionBids = 0
    self.currentAuctions = 0
    self.wonAuctions = 0 # maybe shouldn't be needed
    self.wonItems = 0
    self.rounds = 0 # not used
    self.currentRound = 0 

  # Bidders will somewhat know the market price based on normal distribution (mean, standardDeviation).
  # Then they will stop to bid at a certain value based on the market price and their aggressiveness,
  # which will also be the maximum bid.
  def setMarketprice(self,price):
    self.marketPrice=price*random.normalvariate(1, 0.03)
    self.stopBid=self.marketPrice*(1 + self.behaviour["aggressiveness"])
    # Print for testing purposes:
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
        genBid = int((self.marketPrice*auction["quantity"]/5) * (1 + self.behaviour["aggressiveness"] * self.marketPriceFactor))

      # Print for testing purposes:
      #print("<from bid()> Bidder",self.id, "genBid: ", genBid, "  |  stopBid: ",self.stopBid*auction["quantity"], "  |  market price: ",self.marketPrice*auction["quantity"], "  |  auction: ", auction["id"], "  |  tempBid: ", tempBid,)
      
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

  def updateMarketFactor(self, mean, standardDeviation):
    self.marketPriceFactor = self.behaviour["marketPriceFactorUpdate"](mean, standardDeviation)
  
  def updateWonItems(self, wonItems):
    self.wonItems += wonItems
    self.wonAuctions += 1

  def lostAuction(self):
    self.auctionsLost += 1
  
  def newRound(self):
    self.currentRound += 1

  # Returns a list of dictionaries with info about how the bidder bids.
  def bidUpdate(self, input):
    satisfiedNeed = 0
    currentItems = 0
    returnList = [] # doesn't include quantity
    tempQuantity = 0
    bidOverOnce = False
    checkOnce = True
    index = 0

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
          self.auctionBids += 1
      else:
        if(0 > currentItems - tempQuantity and checkOnce):
          bidOverOnce = True
          checkOnce = False
        if(bid[1]["user"] == self.id):
          continue
        elif(0 < currentItems and bidOverOnce or 0 < currentItems - tempQuantity + bidList[index+1][1]["quantity"]):
          returnList.append({'id' : bid[1]["id"], 'user' : self.id, 'top_bid' : bid[0]})
          self.auctionBids += 1
          bidOverOnce = False
      index += 1

    # Check if the bidder should bid based on the desperation.
    # If the current round is the last round, then the bidder must place a bid if the needs isn't satisfied.
    if(self.behaviour["desperation"](self.currentRound, self.maxRound) == 0  and 0 < currentItems):
      return returnList
    # If the desperation is high, then the bidder will try to bid.
    if(self.behaviour["desperation"](self.currentRound, self.maxRound) > random.random() and 0 < currentItems):
      return returnList

    return []

class Needs:
  def __init__(self, amount, type):
    self.amount = amount
    self.type = type

# Testing method for testing different behaviours.
def test():
  maxRound = 5
  bidder1 = Bidder('1', Needs(55, "steel beam"), maxRound, Behaviour.A)
  bidder2 = Bidder('2', Needs(55, "steel beam"), maxRound, Behaviour.B)
  bidder3 = Bidder('3', Needs(55, "steel beam"), maxRound, Behaviour.C)
  bidder4 = Bidder('4', Needs(55, "steel beam"), maxRound, Behaviour.C)

  print("Created 3 bidders with behaviour type A, B and C respectively and an extra bidder with type C.")
  print("-----------------------------------------------------------------")

  print("Testing the bidUpdate() function:")
  simList = [{'id' : '1', 'quantity' : 40, 'user':'N/A' , 'top_bid' : 16000},
             {'id' : '2', 'quantity' : 55, 'user':'N/A' , 'top_bid' : 13000},
             {'id' : '3', 'quantity' : 40, 'user':'N/A' , 'top_bid' : 11000},
             {'id' : '4', 'quantity' : 50, 'user':'N/A' , 'top_bid' : 12000}]
  simList2 = [{'id': '63f6c3df7b6103af971aba61', 'quantity': 44, 'user': 'N/A', 'top_bid': 13000},
              {'id': '63f6c3e07b6103af971aba63', 'quantity': 41, 'user': 'N/A', 'top_bid': 0}]

  for i in range(1):
    bidder1.newRound()
    bidder3.newRound()
    bidder4.newRound()

  bidder1.setMarketprice(275)
  bidder3.setMarketprice(275)
  bidder4.setMarketprice(275)

  bidder1Info = bidder1.bidUpdate(simList)
  bidder3Info = bidder3.bidUpdate(simList)
  bidder4Info = bidder4.bidUpdate(simList)

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

