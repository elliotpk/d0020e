# Receives a number of sellers with chains of blocks of decreasing price that contain a certain amount of product per block. 
# Also receives a number of buyers with different demands for amounts of products. One has to buy the previous blocks in a chain of blocks to access the later cheaper ones.
# If only block 1 is bought then block 2 will take on the price of block 1 and 3 of 2 and so on. 
# All possible distributions of these are then tested and the one with the best Raj Jain fairness index is choosen and returned/printed.

from itertools import combinations
from itertools import permutations
from Block import *
from Bidder import Bidder
import math
from collections import deque

# Method used:
# 1. Extract all the blocks from the sellers and place these in a list
# 2. Find the permutations of this list using itertools.permutations
# 3. For these permutations: rotate the list n times (this way we don't have to go through all the permutations, only the first n/2)
# 4. For each of the rotations: Find all ways to split the list into a number of sublist equal to the amount of buyers plus one to represent unbought blocks. The "unboughts" can be empty but every buyer will need at least one block to satisfy their demand.
# 5. For each of the ways to split the list (the combinations): Check if this way to split the list gives each buyer a set of blocks that satisfies their demand and in which no block that is among one of the buyers sublist has earlier blocks from their chain in the "unboughts".
# 6. For every combination that passes this: Calculate the average price paid for blocks and calculate Raj Jain Fairness value for this. Save the highest fairness value recieved and return it along with the average price paid by all buyers in that combination (the "market price").    

# sellerlist: A list of the sellers, is immediately converted to a long list of all of their blocks.
# buyers: A list of buyers.
# outputAllCombinations: If set to true the function will output a CSV-file "refcalcOutdata.csv" that lists a matrix for each valid way for the buyers to buy the sellers blocks (fullfilled demands).
def referenceCalculator(sellerlist, buyers, outputAllCombinations = False):
    blocklist = getAllBlocks(sellerlist)
    bestRajJainCostFairness = -1 # -1 returned if no valid combinations can be found, for example if total demand is higher than total supply
    bestData = ""
    allCombinationData = "" # For if one wants to output all the combinations
    permNum = 0
    permAndComb = 0
    averageCostsForBuyers = []
    bestAverageCostsForBuyers = []
    
    print("Beginning reference calculation,", int((len(blocklist)/2)+1) * math.comb(len(blocklist), len(buyers)) * len(blocklist), "combinations to test")
    
    for permutation in permutations(blocklist):
        for rotationOfPermutation in tupleRotatorLister(permutation):
            for combination in splitfinder(rotationOfPermutation, len(buyers)):
                if(validCombination(combination, buyers)):
                    averageCostsForBuyers = []
                    i = 0
                    while i < len(combination)-1: # Runs through what the buyers have bought (the last index is the "unboughts")
                        averageCostsForBuyers.append(averageCost(combination[i]))
                        i = i + 1
                        
                    RajJainCostFairness = rajJainFairness(averageCostsForBuyers)
                    if (RajJainCostFairness > bestRajJainCostFairness):
                        bestRajJainCostFairness = RajJainCostFairness
                        bestAverageCostsForBuyers = averageCostsForBuyers
                    if (outputAllCombinations):
                        allCombinationData = allCombinationData + formatCombination(combination,buyers,sellerlist,averageCostsForBuyers,RajJainCostFairness)
                permAndComb = permAndComb + 1
        permNum = permNum + 1
        print("Permutation number ", permNum, "out of", int((len(blocklist)/2)+1), "Combinations tested:", permAndComb)
        if (permNum > len(blocklist)/2): # Due to the way permutations are listed in the permutation-function this will have tested all relevant possibilities given that the lists have also been rotated.
            break
        
    if (outputAllCombinations):
            outputCombinations(allCombinationData, sellerlist)
    return bestRajJainCostFairness, sum(bestAverageCostsForBuyers)/len(buyers)


# Helper function that takes in a list and returns a list of all rotations of that list.
def tupleRotatorLister(tup):
    rotations = len(tup)
    rotList = []
    tup = deque(tup)

    while(rotations > 0):
        rotList.append(tuple(tup))
        tup.rotate(1)
        rotations = rotations - 1

    return rotList


# Find all possible ways to split the blocks between the buyers (including one "buyer" for unbought blocks)
# Assumes that only the "unbought" blocks can be empty since every buyer should have a demand
# blocklist = All the blocks from the seller arranged in a specific permutation
def splitfinder(blocklist, numBuyers):
    possibleSplits = []
    for breakpoints in combinations(range(1, len(blocklist)+1), numBuyers):  # Combinatorics: find all places to place splitpoints between groups
        possibilityN = []
        
        possibilityN.append(list(blocklist[0:breakpoints[0]]))
        for i in range(0, numBuyers-1):
            possibilityN.append(list(blocklist[breakpoints[i]:breakpoints[i+1]]))
        possibilityN.append(list(blocklist[breakpoints[(len(breakpoints)-1)]:(len(blocklist))]))
        
        possibleSplits.append(list(possibilityN))
    return possibleSplits


# Takes in a way to split the blocks between the buyers and returns whether what they have bought is allowed and whether their demand is fullfilled
# combination = A list of lists in which each list is what block have been bought by a buyer except the last list which is the "unbought" blocks.
# buyers = A list of all the buyers
def validCombination(combination, buyers):
    possibleCombination = combination.copy() # To prevent the original list from being changed through references
    unboughts = possibleCombination.pop()
    for unboughtBlock in unboughts:
        if(checkIfPreviousBlockUnbought(unboughtBlock, possibleCombination) == False): # Blocks that have been bought cannot have blocks that stand before them in order not be bought since this would invalidate the sales from buying several blocks.
            return False
    
    buyerIndex = 0
    for buyerBoughts in possibleCombination: # All buyers demands must also be fullfilled
        demand = buyers[buyerIndex].needs.amount
        for block in buyerBoughts:
            demand = demand - block.get_amount()
        if(demand > 0):
            return False
        buyerIndex = buyerIndex + 1
            
    return True

    
# Recursively check if a block that has to be bought after another block has been bought without this being the case
def checkIfPreviousBlockUnbought(unboughtBlock, boughtBlocks):    
    if(unboughtBlock.next() != None):
        for blockset in boughtBlocks:
            if(unboughtBlock.next() in blockset):
                return False            
        return checkIfPreviousBlockUnbought(unboughtBlock.next(), boughtBlocks)
    else:
        return True
    
    
# Calculation of Raj Jain's fairness index following the equation (taken from Wikipedia)
# metricList = A list containing a series of numbers to compare fairness between. For example a list of the average price each buyer has had to pay for their blocks.
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


# Feed this function a valid set of blocks for a buyer to buy and it will return the average cost paid
def averageCost(boughtBlocks):
    sum = 0
    totAmount = 0
    for block in boughtBlocks:
        discount = findDiscount(block,boughtBlocks)
        sum = sum + (block.get_amount() * (block.get_price()/block.get_amount() * (1-(discount/100))))
        totAmount = totAmount + block.get_amount()
    return sum / totAmount


# Finds the discount that should be applied to a given block recursivly under the assumption that block.discount is the cumulative discount on a base price given all previous blocks are bought 
# Block = Block discount is sought for, boughtBlocks = The blocks bought by a buyer, foundPrevBlocks = recursion variable, init at 0
# Goes back to the beginning of the sellers blockchain, finding how many blocks in that chain have been purchased. Then goes to the "index" in that blockchain that 
# corresponds to the number of blocks found, there finding the discount of if the block had been moved to that place in the chain.
def findDiscount(block, boughtBlocks, foundPrevBlocks = 0):
    if (block.prev() != None):
        if(block.prev() in boughtBlocks):
            foundPrevBlocks = foundPrevBlocks + 1
        return findDiscount(block.prev(), boughtBlocks, foundPrevBlocks)
    else:
        discount = 0
        while foundPrevBlocks > 0:
            discount = block.next().get_discount()
            block = block.next()
            foundPrevBlocks = foundPrevBlocks - 1
        return discount


# Extracts all the blocks from the sellers it is given.
def getAllBlocks(sellerlist):
    blocklist = []
    for seller in sellerlist:
        SellerBlocklist=seller.LinkOfBlocks.display()
        for block in SellerBlocklist:
            blocklist.append(block)
    return blocklist


# Takes in data that is assumed to be relevant for analysis and formats this as a CSV file.
# combination = a valid way of distributing blocks among the buyers (with one extra "buyer" for the "unbought" blocks).
# All the input data is attainable inside the referenceCalculator function.
def formatCombination(combination, buyerslist, sellerlist, averageCosts, rajJainFairness):
    combinationWithoutUnboughts = combination.copy()
    unboughts = combinationWithoutUnboughts.pop() # Reference to unbought blocks saved in case this is interesting in the future
    outstring = ""

    # Each field in the intersection of a seller column and a buyer row is filled with the blocks purchased from that seller by that buyer. 
    i = 1
    for blockset in combinationWithoutUnboughts:
        outstring = outstring + "Buyer " + str(i) + ","
        for seller in sellerlist:
            for block in blockset:
                if block in seller.LinkOfBlocks.display():
                    outstring = outstring + r" [$=" + str(round(block.get_price() * (1-(findDiscount(block,combinationWithoutUnboughts)/100)))) + " x=" + str(block.get_amount()) + " d=" + "dist" + "]"
            outstring = outstring + ","
        outstring = outstring + str(averageCosts[i-1]) + "," + "avgDist" + "," + str(rajJainFairness)
        outstring = outstring + "\n"
        i = i + 1
    
    return outstring


# Writes the data to a file, beginning with columns. Will overwrite old output file.
def outputCombinations(allCombinationData, sellerlist, filename = "refcalcOutdata.csv"):
    columns = "Buyers,"  # Column creation
    i = 1
    for seller in sellerlist:
        columns = columns + "Seller " + str(i) + ","
        i = i + 1
    columns = columns + "AveragePrice, AverageDistance, RaijJainFairness\n"

    try:
        outfile = open(filename, "w")
        outfile.write(columns)
        outfile.close
        outfile = open(filename, "a")
        outfile.write(allCombinationData)
        outfile.close
    except:
        print("RefCalc file error")


# Maths equation for total iterations using naive given n blocks and b bidders: n! * nCb = n!^2/(b!(n-b)!).
# Using the method with rotating lists we instead get n^2/2 * nCb