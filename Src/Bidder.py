#class Buyers/bidders
import Behaviour

class Bidder:
  def __init__(self, id, name, amount, needs, behaviour, marketPrice):
    self.id = id
    self.name = name
    self.initAmount = amount
    self.currentAmount = amount
    self.needs = needs
    self.behaviour = behaviour
    self.currentAuctions = 0
    self.winningAuctions = 0
    self.marketPrice = marketPrice

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


# Demonstration:

bidder1 = Bidder(1, "John Andersson", 150000, Needs(55, "steel beam"), Behaviour.A, 15000)

print("Created: Bidder ",bidder1.id,"\n",
      "name: ",bidder1.name,"\n",
      "amount: ",bidder1.initAmount,"\n",
      "needs (amount): ",bidder1.needs.amount,"\n",
      "needs (type): ",bidder1.needs.type,"\n",
      "behaviour: ",bidder1.behaviour,"\n",
      "currentAuctions: ",bidder1.currentAuctions,"\n",
      "winning auctions: ",bidder1.winningAuctions,"\n",
      "market price: ",bidder1.marketPrice)

# the bidder participates in 2 auctions:

# the bidder doesn't want to bid because it's not a discount
if(bidder1.behaviour["onlyBidDiscounts"] == False):
  bidder1.setCurrentAuctions(2)
else:
  bidder1.setCurrentAuctions(2)
  bidder1.setWinningAuctions(1)
  bidder1.setCurrentAmount(50000)

print("Updated: Bidder ",bidder1.id,"\n",
      "name: ",bidder1.name,"\n",
      "amount: ",bidder1.currentAmount,"\n",
      "needs (amount): ",bidder1.needs.amount,"\n",
      "needs (type): ",bidder1.needs.type,"\n",
      "behaviour: ",bidder1.behaviour,"\n",
      "currentAuctions: ",bidder1.currentAuctions,"\n",
      "winning auctions: ",bidder1.winningAuctions,"\n",
      "market price: ",bidder1.marketPrice)