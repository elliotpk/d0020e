#Library, module
import random
import math

# Returns one random behaviour.
# Note: new behaviours must be added in the list.
def randomBehaviour():
  behaviourList = [A, B, C]
  return random.choice(behaviourList)

def getBehaviour(input):
    if input == A["behaviour"]:
        return A
    elif input == B["behaviour"]:
        return B
    elif input == C["behaviour"]:
        return C
    else:
        return randomBehaviour()

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
                            changeAggressiveness(A, 1.0) if(maxRound - currentRound == 0) else
                            changeAggressiveness(A, A["aggressiveness"]) if(currentRound/maxRound >= 0.90) else
                            changeAggressiveness(A, A["aggressiveness"]) if(currentRound/maxRound >= 0.75) else
                            changeAggressiveness(A, A["aggressiveness"]) if(currentRound/maxRound >= 0.50) else
                            changeAggressiveness(A, A["aggressiveness"]) if(currentRound/maxRound >= 0.25) else
                            changeAggressiveness(A, A["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       0 if(maxRound == currentRound) else
                       A["aggressiveness"]*currentRound/maxRound,
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
                            changeAggressiveness(B, 1.0) if(maxRound - currentRound == 0) else
                            changeAggressiveness(B, 0.9) if(currentRound/maxRound >= 0.90) else                            
                            changeAggressiveness(B, 0.8) if(currentRound/maxRound >= 0.75) else
                            changeAggressiveness(B, 0.7) if(currentRound/maxRound >= 0.50) else
                            changeAggressiveness(B, 0.6) if(currentRound/maxRound >= 0.25) else
                            changeAggressiveness(B, B["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       0 if(maxRound == currentRound) else
                       B["aggressiveness"]*currentRound/maxRound,
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
                            changeAggressiveness(C, 1.0) if(maxRound - currentRound == 0) else
                            changeAggressiveness(C, 0.8) if(currentRound/maxRound >= 0.90) else
                            changeAggressiveness(C, 0.6) if(currentRound/maxRound >= 0.75) else
                            changeAggressiveness(C, 0.4) if(currentRound/maxRound >= 0.50) else
                            changeAggressiveness(C, 0.3) if(currentRound/maxRound >= 0.25) else
                            changeAggressiveness(C, C["aggressiveness"]),
  "desperation": lambda currentRound, maxRound:
                       0 if(maxRound == currentRound) else
                       C["aggressiveness"]*currentRound/maxRound,
  "bidOverMarketPrice": True,
  "marketPriceFactor": 1.0,
  "marketPriceFactorUpdate": lambda mean, standardDeviation:
                             marketPriceFactor(C, C["aggressiveness"], mean, standardDeviation),
  "stopBid": lambda marketPrice:
             marketPrice*(1 + C["aggressiveness"])
} 