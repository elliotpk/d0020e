#Library, module
import random

# Returns one random behaviour.
# Note: new behaviours has to be added in the list.
def randomBehaviour():
  behaviourList = [A, B, C]
  return random.choice(behaviourList)

# Returns k random behaviours with weighted possibilities.
# Example: weights = [1,10] means that the selection chance is 10 times bigger for the second behaviour.
# Note: new behaviours has to be added in the list.
def randomBehaviourAdvanced(weights, k):
  behaviourList = [A, B, C]
  return random.choices(behaviourList, weights = weights, k = k)

# Desperate behaviour, always bids max amount.
# Can bid over the market value, but not over the maximum amount.
# The chance of bidding on any number of blocks are the same.
A = {
  "behaviour": "A",
  "onlyBidMaxAmount": True,
  "bidMaxBlocks": 3,
  "blockBehaviour": lambda blocks:
                    True if (blocks == 3) else
                    True if (blocks == 2) else
                    True if (blocks == 1) else
                    False ,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else
         # Can bid over market value
         True if (price > marketPrice) else 
         (price < currentAmount)
}

# Doesn't bid if it's more than 2 blocks, over the market value or over the maximum amount.
# It has 100% chance of bidding if there are 2 blocks instead of 50% if it's only 1 block.
B = {
  "behaviour": "B",
  "onlyBidMaxAmount": False,
  "bidMaxBlocks": 2,
  "blockBehaviour": lambda blocks:
                    False                  if (blocks == 3) else
                    True                   if (blocks == 2) else
                    0.5 <= random.random() if (blocks == 1) else
                    False ,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < currentAmount)
} 

# Minimal bidding behaviour.
# Doesn't bid if it's more than 1 block, over the market value or over the maximum amount.
C = {
  "behaviour": "C",
  "onlyBidMaxAmount": False,
  "bidMaxBlocks": 1,
  "blockBehaviour": lambda blocks:
                    False                  if (blocks == 3) else
                    False                  if (blocks == 2) else
                    True                   if (blocks == 1) else
                    False ,
  "bid": lambda price, marketPrice, currentAmount:
         # Can't bid over budget
         False if (price > currentAmount) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < currentAmount)
} 