import APILink
import Block

class Sellers:

    def __init__(self,id):
        self.id = id
        self.auctionId = []
        self.quantity = []
        self.LinkOfBlocks = Block.LinkOfBlocks()

    def createAuction(self):
        try:
            for x in self.quantity:
                roomid=APILink.createAuction(str(self.id),"Seller",x)
                self.auctionId.append(roomid)
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
        block.set_Object = "Block " + str(price) + " " + str(amount) + " " + str(discount) # For debugging mostly
        self.LinkOfBlocks.add(block)
        block.set_discount(discount + block.prev().get_discount())

