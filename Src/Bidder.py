import Behaviour

class Bidder:
  def __init__(self, id, amount, needs, marketPrice, behaviour):
    self.id = id
    self.initAmount = amount
    self.currentAmount = self.initAmount
    self.needs = needs
    self.marketPrice = marketPrice
    self.behaviour = behaviour
    self.currentAuctions = 0
    self.winningAuctions = 0
    

  def setCurrentAuctions(self, currentAuctions):
    self.currentAuctions = currentAuctions

  def setWinningAuctions(self, winningAuctions):
    self.winningAuctions = winningAuctions

  def setCurrentAmount(self, amount):
    self.currentAmount = amount


class Needs:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

# Testing function for testing different behaviours
def test():
  bidder1 = Bidder(1, 150000, Needs(55, "steel beam"), 15000, Behaviour.A)
  bidder2 = Bidder(2, 150000, Needs(55, "steel beam"), 15000, Behaviour.B)

  print("Created: Bidder ",bidder1.id,"\n",
        "amount: ",bidder1.initAmount,"\n",
        "needs (amount): ",bidder1.needs.amount,"\n",
        "needs (type): ",bidder1.needs.type,"\n",
        "behaviour: ",bidder1.behaviour["behaviour"],"\n",
        "currentAuctions: ",bidder1.currentAuctions,"\n",
        "winning auctions: ",bidder1.winningAuctions,"\n",
        "market price: ",bidder1.marketPrice)

  print("Created: Bidder ",bidder2.id,"\n",
        "amount: ",bidder2.initAmount,"\n",
        "needs (amount): ",bidder2.needs.amount,"\n",
        "needs (type): ",bidder2.needs.type,"\n",
        "behaviour: ",bidder2.behaviour["behaviour"],"\n",
        "currentAuctions: ",bidder2.currentAuctions,"\n",
        "winning auctions: ",bidder2.winningAuctions,"\n",
        "market price: ",bidder2.marketPrice)

  # Bidder 1 participates in 2 auctions:
  # Bidder 1 will bid the max amount in one of the auctions because of desperate behaviour.
  # Bidder 1 can bid because the price is lower than the maximum amount that the bidder have.
  print("-----------------------------------------------------------------")
  if(bidder1.behaviour["onlyBidMaxAmount"] == True
     and
     bidder1.behaviour["bid"](14000, bidder1.marketPrice, bidder1.currentAmount)
    ):
    bidder1.setCurrentAuctions(2)
    bidder1.setWinningAuctions(1)
    bidder1.setCurrentAmount(0)
    print("Bidder ",bidder1.id," bid the max amount in 1 auction.")
  else:
    bidder1.setCurrentAuctions(2)
    print("Bidder ",bidder1.id," didn't bid in any auction.")
  # Restore the initial amount.
  bidder1.setCurrentAmount(bidder1.initAmount)

  # Tests that can make a bidder bid differently based on what a bidder knows
  # about price, market price (15000) and the maximum amount.
  print("-----------------------------------------------------------------")
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

  print("Test if bidder 2 bids if it's less than 3 blocks:")
  if(bidder2.behaviour["bidMaxBlocks"] < 3
     and
     bidder2.behaviour["bid"](14000, bidder2.marketPrice, bidder2.currentAmount)
    ):
    bidder2.setCurrentAuctions(2)
    bidder2.setWinningAuctions(1)
    bidder2.setCurrentAmount(0)
    print("Bidder ",bidder2.id," bid in 1 auction with less than 3 blocks.")
  else:
    bidder2.setCurrentAuctions(2)
    print("Bidder ",bidder2.id," didn't bid in any auction.")
  # Restore the initial amount.
  bidder2.setCurrentAmount(bidder2.initAmount)
  print("-----------------------------------------------------------------")

  print("Test 100 times if bidder 2 wants to bid if it's only 1 block (50 percent chance):")
  counter = 0
  for x in range(100):
    if(bidder2.behaviour["blockBehaviour"](1)
      and
      bidder2.behaviour["bid"](14000, bidder2.marketPrice, bidder2.currentAmount)
      ):
      bidder2.setCurrentAuctions(2)
      bidder2.setWinningAuctions(1)
      bidder2.setCurrentAmount(0)
      counter = counter + 1
    else:
      bidder2.setCurrentAuctions(2)
    # Restore the initial amount.
    bidder2.setCurrentAmount(bidder2.initAmount)

  print("Bidder ", bidder2.id, "bid ", counter, " times out of 100.")

test()
