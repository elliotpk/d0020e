#Library, module
import random

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
def marketPriceFactor(aggressiveness, mean, standardDeviation):
  return aggressiveness*random.normalvariate(mean, standardDeviation)

# Very aggressive behaviour, always bids max amount.
# The aggressiveness stays the same for this behaviour.
# Can bid over the market value, but not over the maximum amount.
A = {
  "behaviour": "A",
  "onlyBidMaxAmount": True,
  "aggressiveness": 0.9,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(A, A["aggressiveness"]),
  "bidOverMarketPrice": True,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else
         # Can bid over market value
         True if (price > marketPrice) else 
         (price < currentAmount),
  "marketPriceFactor": lambda mean, standardDeviation:
                       marketPriceFactor(A["aggressiveness"], mean, standardDeviation)
}

# Medium aggressive behaviour.
# Aggressiveness increases when the auctions lost increases or
# when there are more than 10 bids in 1 participated auction.
# Doesn't bid if it's over the market value or over the maximum amount.
B = {
  "behaviour": "B",
  "onlyBidMaxAmount": False,
  "aggressiveness": 0.5,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(B, 0.8) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(B, 0.7) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(B, 0.6) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(B, 0.6) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(B, B["aggressiveness"]),
  "bidOverMarketPrice": False,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < currentAmount),
  "marketPriceFactor": lambda mean, standardDeviation:
                       marketPriceFactor(B["aggressiveness"], mean, standardDeviation)
} 

# Minimal and passive bidding behaviour.
# Aggressiveness increases when the auctions lost increases or
# when there are more than 10 bids in 1 participated auction.
# Doesn't bid if it's over the market value or over the maximum amount.
C = {
  "behaviour": "C",
  "onlyBidMaxAmount": False,
  "aggressiveness": 0.1,
  "adaptiveAggressiveness": lambda auctions, auctionsLost, currentBids:
                            changeAggressiveness(C, 0.6) if(auctions > 4 and auctionsLost > 3 and currentBids >= 0) else
                            changeAggressiveness(C, 0.4) if(auctions > 3 and auctionsLost > 2 and currentBids >= 0) else
                            changeAggressiveness(C, 0.2) if(auctions > 2 and auctionsLost > 1 and currentBids >= 0) else
                            changeAggressiveness(C, 0.2) if(auctions == 1 and currentBids > 10) else
                            changeAggressiveness(C, C["aggressiveness"]),
  "bidOverMarketPrice": False,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < currentAmount),
  "marketPriceFactor": lambda mean, standardDeviation:
                       marketPriceFactor(C["aggressiveness"], mean, standardDeviation)
} 