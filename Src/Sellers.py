
import random

class Sellers:

    def __init__(self):
        self.hasAuction = False
        self.blockList = Block

    def createAuction(self):
        #Api call create auction
        self.hasAuction = True

    def genBlockList(self,blocks):
        List = []
        for x in range(blocks):
            price=random.randrange(10,100)
            amount=random.randrange(10,100)
            List.append(Block(price,amount))
        for x in range(len(List)):
            try:
                List[x].nextblock=List[x+1]
            except:
                List[x].nextblock=None
        self.blockList = List[0]


class Block:

    def __init__(self,price,amount):
        self.price = price
        self.amount = amount
        self.nextblock = Block

