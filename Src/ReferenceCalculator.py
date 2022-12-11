#calc(numSellers,buyers,blocks) returns marketvalue/print CSV

# Receives a number of sellers with chains of blocks of decreasing price that contain a certain amount of product per block. 
# Also receives a number of buyers with different demands for amounts of products. One has to buy the previous blocks in a chain of blocks to access the later cheaper ones.
# If only block 1 is bought then block 2 will take on the price of block 1 and 3 of 2 and so on. 
# All possible distributions of these are then tested and the one with the best Raj Jain fairness index is choosen and returned/printed.

# Note: The sellers themselves should not matter, only their blockchains. 

from itertools import combinations

# blocklist: All the blocks together in a list (since the linked block class is not yet finished. Either one later changes the code to use these instead or adds a funtion to convert the linked list to an ordinary one)
# buyers: A list of buyers.
def referenceCalculator(blocklist, buyers):
    #splitfinder to find all combinations
    
    #round-robin with the buyers so that all buyers test all combinations, do this by switching their indexes probably 
    
    #test the validity of all the combinations (not buying a block with a previous block unbought, (demand fullfilled?))
    
    #for the valid combinations: calculate the average price each buyer paid and place these in a list
    
    #feed this list to the Raj Jain Fairness method and place the result in a big list together with other relevant data for each tried combination
    
    #after every combination: sort the list and return the highest fairness index
    
    #Make all of this modular so that the Fairness Index is easily switched to something else.
    return
    

# Find all possible ways to split the blocks between the buyers (including one "buyer" for unbought blocks)
def splitfinder(blocklist, numBuyers):
    
    possibleSplits = []
    for breakpoints in combinations(range(1, len(blocklist)), numBuyers):  # Combinatorics: find all places to place splitpoints between groups
        possibilityN = []
        
        possibilityN.append(list(blocklist[0:breakpoints[0]]))
        for i in range(0, numBuyers-1):
            possibilityN.append(list(blocklist[breakpoints[i]:breakpoints[i+1]]))
        possibilityN.append(blocklist[breakpoints[(len(breakpoints)-1)]:(len(blocklist))])
        
        possibleSplits.append(list(possibilityN))
    
    return possibleSplits

# Takes in a way to split the blocks between the buyers and returns whether what they have bought is allowed (and fullfills everyones demand, at least until we've clarified that)
def validCombination(possibleCombination, buyers):
    unboughts = possibleCombination.pop()
    
    for unboughtBlock in unboughts:
        if(checkIfPreviousBlockUnbought(unboughtBlock, possibleCombination) == False):
            return False
    
    buyerIndex = 0
    for buyerBoughts in possibleCombination:
        demand = buyers[buyerIndex].needs.amount
        for block in buyerBoughts:
            demand = demand - block.amount
        if(demand > 0):
            return False
    buyerIndex = buyerIndex + 1
            
    return True
    
# Recursively check if a block that has to be bought after another block has been bought without this being the case
def checkIfPreviousBlockUnbought(unboughtBlock, boughtBlocks):    
    if(unboughtBlock.next != None):
        for blockset in boughtBlocks:
            if(unboughtBlock.next in blockset):
                return False
            else:
                return checkIfPreviousBlockUnbought(unboughtBlock.next, boughtBlocks)
    else:
        return True
    
# Calculation of Raj Jain's fairness index following Wikipedia equation
def rajJainFairness(metricList):
    numerator = 0
    denominator = 0
    for metric in metricList:
        numerator = numerator + metric
        denominator = denominator + (metric**2)
        
    numerator = numerator**2
    denominator = denominator * len(metricList)
    
    fairnessIndex = numerator / denominator
    return fairnessIndex

def averageCost():
    return

def demo():
    blocklist = ["block11", "block12", "block21", "block31"]
    buyers = 2
    #blocklist = ["block11", "block12", "block13", "block21", "block22", "block31"]
    #buyers = 3
    
    splits = splitfinder(blocklist, buyers)
    print("\nPossible combinations:")
    for split in splits:
        print(split)
    
    
    demoMetrics = [10, 10, 10, 10, 10]    
    #demoMetrics = [5.5, 10, 7.6, 3]
    #demoMetrics = [121, 220, 150, 89, 95, 140, 190]
    
    print("\n Rai Jain's fairness index given the input", demoMetrics, "\n", rajJainFairness(demoMetrics), "\n")

demo()
    