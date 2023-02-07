import APILink
import random
import Block
class Sellers:

    def __init__(self,id):
        self.id = id
        self.auctionId = self.createAuction()
        self.LinkOfBlocks = Block.LinkOfBlocks()

    def createAuction(self):
        try:
            roomid=APILink.createAuction(str(self.id),"Seller",10)
        except:
            roomid=None
        return roomid

    def genBlock(self,price,amount,discount):
        self.LinkOfBlocks.head.set_price(price)
        self.LinkOfBlocks.head.set_amount(amount)
        self.LinkOfBlocks.head.set_discount(discount)
        self.LinkOfBlocks.head.set_Object("Block")

    def addBlock(self,price,amount,discount):
        block=Block.AuctionBlock()
        block.set_price(price)
        block.set_amount(amount)
        block.set_discount(discount)
        block.set_Object = "Block " + str(price) + " " + str(amount) + " " + str(discount) # For debugging mostly
        self.LinkOfBlocks.add(block)




