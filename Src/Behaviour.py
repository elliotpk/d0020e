#Library, module
import random
import math

# Returns one random behaviour.
# Note: new behaviours must be added in the list.
def randomBehaviour():
  behaviourList = [A, B, C]
  return random.choice(behaviourList)

# Returns k random behaviours with weighted possibilities.
# Example: weights = [1, 10, 1] means that the selection chance is 10 times bigger for the second behaviour.
# Note: new behaviours must be added in the list.
def randomBehaviourAdvanced(weights, k):
  behaviourList = [A, B, C]
  return random.choices(behaviourList, weights = weights, k = k)

# This function updates and returns the aggressiveness value of a certain behaviour.
# Note: this function should only be used in the Behaviour library.
def changeAggressiveness(behaviour, value):
  behaviour["aggressiveness"] = value
  return value

# This function returns a factor that is used for bidding based on the market price.
# It uses a normal distribution since it's more common to bid in certain scenarios.
# Note: if the factor is 0 or negavtive, the calculation repeats until it's positive,
# therefore avoid standard deviation integers close to 1/2 of the mean value for accurate normal distribution results.
def marketPriceFactor(behaviour, aggressiveness, mean, standardDeviation):
  behaviour["marketPriceFactor"] = aggressiveness*random.normalvariate(mean, standardDeviation)
  while behaviour["marketPriceFactor"] <= 0 :
    behaviour["marketPriceFactor"] = aggressiveness*random.normalvariate(mean, standardDeviation)
  return behaviour["marketPriceFactor"]

# Very aggressive behaviour, always bids max amount.
# The aggressiveness stays the same for this behaviour currently.
# Can bid over the market value.
A = {
  "behaviour": "A",
  "aggressiveness": 0.9,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(A, A["aggressiveness"]),
  "roundsBehaviour" : lambda rounds:
                      math.pow(A["aggressiveness"], rounds),
  "bidOverMarketPrice": True,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(A, A["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + A["aggressiveness"])
}

# Medium aggressive behaviour.
# Aggressiveness increases when there are more auctions to bid on and how many auctions that is lost
# or when there are more than 10 bids in 1 participated auction.
# Doesn't bid if it's over the market value.
B = {
  "behaviour": "B",
  "aggressiveness": 0.5,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(B, 0.8) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(B, 0.7) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(B, 0.6) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(B, 0.6) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(B, B["aggressiveness"]),
  "roundsBehaviour" : lambda rounds:
                      math.pow(B["aggressiveness"], rounds),
  "bidOverMarketPrice": False,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(B, B["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + B["aggressiveness"])
} 

# Minimal and passive bidding behaviour.
# Aggressiveness increases when there are more auctions to bid on and how many auctions that is lost
# or when there are more than 10 bids in 1 participated auction.
# Doesn't bid if it's over the market value.
C = {
  "behaviour": "C",
  "aggressiveness": 0.1,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(C, 0.6) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(C, 0.4) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(C, 0.2) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(C, 0.2) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(C, C["aggressiveness"]),
  "roundsBehaviour" : lambda rounds:
                      math.pow(C["aggressiveness"], rounds),
  "bidOverMarketPrice": False,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(C, C["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + C["aggressiveness"])
} 