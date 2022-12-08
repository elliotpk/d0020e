#class Buyers/bidders
import Behaviour

class Bidder:
  def __init__(self, id, amount, needs, behaviour, currentAuctions, winningAuctions, marketPrice):
    self.id = id
    self.amount = amount
    self.needs = needs
    self.behaviour = behaviour
    self.currentAuctions = currentAuctions
    self.winningAuctions = winningAuctions
    self.marketPrice = marketPrice

class Needs:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type


# Demonstration:

needsBidder1 = Needs(55, "steel beam")
bidder1 = Bidder(1, 150000, needsBidder1, Behaviour.A, 1, 0, 15000)

print("Created: Bidder ",bidder1.id,"\n",
      "amount: ",bidder1.amount,"\n",
      "needs (amount): ",needsBidder1.amount,"\n",
      "needs (type): ",needsBidder1.type,"\n",
      "behaviour: ",bidder1.behaviour,"\n",
      "currentAuctions: ",bidder1.currentAuctions,"\n",
      "winning auctions: ",bidder1.winningAuctions,"\n",
      "market price: ",bidder1.marketPrice)
