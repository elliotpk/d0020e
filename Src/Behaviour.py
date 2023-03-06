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
  "adaptiveAggressiveness": lambda currentRound, maxRound:
                            changeAggressiveness(A, A["aggressiveness"]) if(maxRound - currentRound == 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(maxRound - currentRound > 1) else
                            changeAggressiveness(A, A["aggressiveness"]) if(maxRound - currentRound > 2) else
                            changeAggressiveness(A, A["aggressiveness"]) if(maxRound - currentRound > 3) else
                            changeAggressiveness(A, A["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       A["aggressiveness"]*(maxRound-currentRound)/maxRound,
  "bidOverMarketPrice": True,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(A, A["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + A["aggressiveness"])
}

# Medium aggressive behaviour.
# Aggressiveness increases when the current round is nearing the last round.
# Can bid over the market value.
B = {
  "behaviour": "B",
  "aggressiveness": 0.5,
  "adaptiveAggressiveness": lambda currentRound, maxRound:
                            changeAggressiveness(B, 0.9) if(maxRound - currentRound == 0) else
                            changeAggressiveness(B, 0.8) if(maxRound - currentRound > 1) else
                            changeAggressiveness(B, 0.7) if(maxRound - currentRound > 2) else
                            changeAggressiveness(B, 0.6) if(maxRound - currentRound > 3) else
                            changeAggressiveness(B, B["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       B["aggressiveness"]*(maxRound-currentRound)/maxRound,
  "bidOverMarketPrice": True,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(B, B["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + B["aggressiveness"])
} 

# Minimal and passive bidding behaviour.
# Aggressiveness increases when the current round is nearing the last round.
# Can bid over the market value.
C = {
  "behaviour": "C",
  "aggressiveness": 0.2,
  "adaptiveAggressiveness": lambda currentRound, maxRound:
                            changeAggressiveness(C, 0.6) if(maxRound - currentRound == 0) else
                            changeAggressiveness(C, 0.5) if(maxRound - currentRound > 1) else
                            changeAggressiveness(C, 0.4) if(maxRound - currentRound > 2) else
                            changeAggressiveness(C, 0.3) if(maxRound - currentRound > 3) else
                            changeAggressiveness(C, C["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       C["aggressiveness"]*(maxRound-currentRound)/maxRound,
  "bidOverMarketPrice": True,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(C, C["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + C["aggressiveness"])
} 