#Library, module
import random

# Returns one random behaviour.
# Note: new behaviours has to be added in the list.
def randomBehaviour():
  behaviourList = [A, B]
  return random.choice(behaviourList)

# Returns k random behaviours with weighted possibilities.
# Example: weights = [1,10] means that the selection chance is 10 times bigger for the second behaviour.
# Note: new behaviours has to be added in the list.
def randomBehaviourAdvanced(weights, k):
  behaviourList = [A, B]
  return random.choices(behaviourList, weights = weights, k = k)

# Desperate behaviour, always bids max amount with and without discounts.
# Can bid over the market value, but not over the maximum amount.
A = {
  "behaviour": "A",
  "onlyBidMaxAmount": True,
  "bidMaxBlocks": 3,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else
         # Can bid over market value
         True if (price > marketPrice) else 
         (price < currentAmount)
}

# Doesn't bid if it's more than 2 blocks, over the market value or over the maximum amount.
B = {
  "behaviour": "B",
  "onlyBidMaxAmount": False,
  "bidMaxBlocks": 2,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < currentAmount)
} 