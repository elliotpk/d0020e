import Behaviour

class Bidder:
  def __init__(self, id, amount, needs, marketPrice, behaviour):
    self.id = id
    self.initAmount = amount
    self.currentAmount = amount
    self.needs = needs
    self.marketPrice = marketPrice
    self.behaviour = behaviour
    self.behaviour["bidMax"] = amount # maybe unneccessary to have a bidMax in behaviour
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

# Demonstration
def demo():
  bidder1 = Bidder(1, 150000, Needs(55, "steel beam"), 15000, Behaviour.A)

  print("Created: Bidder ",bidder1.id,"\n",
        "amount: ",bidder1.initAmount,"\n",
        "needs (amount): ",bidder1.needs.amount,"\n",
        "needs (type): ",bidder1.needs.type,"\n",
        "behaviour: ",bidder1.behaviour,"\n",
        "currentAuctions: ",bidder1.currentAuctions,"\n",
        "winning auctions: ",bidder1.winningAuctions,"\n",
        "market price: ",bidder1.marketPrice)

  # The bidder participates in 2 auctions:
  # The bidder will bid the max amount in one of the auctions because of desperate behaviour.
  # The bidder can bid because the price is lower than the maximum amount that the bidder have.
  if(bidder1.behaviour["onlyBidMaxAmount"] == True
     &
     bidder1.behaviour["bid"](14000,bidder1.marketPrice, bidder1.behaviour["bidMax"])
    ):
    bidder1.setCurrentAuctions(2)
    bidder1.setWinningAuctions(1)
    bidder1.setCurrentAmount(0)
    print("Bidder ",bidder1.id," bid the max amount in 1 auction.")
  else:
    bidder1.setCurrentAuctions(2)
    print("Bidder ",bidder1.id," didn't bid in any auction.")

  # Tests that can make the bidder bid differently based on what the bidder knows
  # about price, market price (15000) and the maximum amount.
  print("-----------------------------------------------------------------")
  print("Bid behaviour test if the bidder can bid or not:")
  # Can bid with Behaviour type A:
  print("Highest to lowest: bidMax, price, marketPrice: ",bidder1.behaviour["bid"](15001,bidder1.marketPrice, bidder1.behaviour["bidMax"]))
  print("Highest to lowest: bidMax, marketPrice, price: ",bidder1.behaviour["bid"](14001,bidder1.marketPrice, bidder1.behaviour["bidMax"]))
  print("Highest to lowest: marketPrice, bidMax, price: ",bidder1.behaviour["bid"](14001,bidder1.marketPrice, 14002))
  # Can't bid with behaviour type A:
  print("Highest to lowest: marketPrice, price, bidMax: ",bidder1.behaviour["bid"](14001,bidder1.marketPrice, 10000))
  print("Highest to lowest: price, marketPrice, bidMax: ",bidder1.behaviour["bid"](15001,bidder1.marketPrice, 10000))
  print("Highest to lowest: price, bidMax, marketPrice: ",bidder1.behaviour["bid"](15002,bidder1.marketPrice, 15000))


demo()
