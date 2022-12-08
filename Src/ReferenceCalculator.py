#calc(numSellers,buyers,blocks) returns marketvalue/print CSV

# Receives a number of sellers with chains of blocks of decreasing price that contain a certain amount of product per block. 
# Also receives a number of buyers with different demands for amounts of products. One has to buy the previous blocks in a chain of blocks to access the later cheaper ones.
# If only block 1 is bought then block 2 will take on the price of block 1 and 3 of 2 and so on. 
# All possible distributions of these are then tested and the one with the best Rai Jain fairness index is choosen and returned/printed.

# Note: The sellers themselves should not matter, only their blockchains. 

# blocklist: A list of a list of blocks (since the linked block class is not yet finished. Either one later changes the code to use these instead or adds a funtion to convert the linked list to an ordinary one)
# buyers: A list of buyers that each say how much they want.
def referenceCalculator(blocklistlist, buyers):
    resetBlocklistlist = blocklistlist
    resetBuyers = buyers
    
    for buyer in buyers:
        for blocklist in blocklistlist:
            print("This will require more thought")
            
             
        
    
    # for blocklist in blocklistlist:
    #     savedPurchasingBlockIndex = -1
    #     for block in blocklist:
    #         i = 0
    #         while i < len(buyers):
                
    #         #for buyer in buyers:
    #         #    if buyer.demand > 0: