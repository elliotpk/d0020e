#class Buyers/bidders
import Behaviour

class Bidder:
  def __init__(self, id, amount, needs, behaviour, marketPrice):
    self.id = id
    self.amount = amount
    self.needs = needs
    self.behaviour = behaviour
    self.currentAuctions = 0
    self.winningAuctions = 0
    self.marketPrice = marketPrice

class Needs:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

# Demonstration:

bidder1 = Bidder(1, 150000, Needs(55, "steel beam"), Behaviour.A, 15000)

print("Created: Bidder ",bidder1.id,"\n",
      "amount: ",bidder1.amount,"\n",
      "needs (amount): ",bidder1.needs.amount,"\n",
      "needs (type): ",bidder1.needs.type,"\n",
      "behaviour: ",bidder1.behaviour,"\n",
      "currentAuctions: ",bidder1.currentAuctions,"\n",
      "winning auctions: ",bidder1.winningAuctions,"\n",
      "market price: ",bidder1.marketPrice)
