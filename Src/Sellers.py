import APILink
#import random
#import Block
class Sellers:

    def __init__(self,id,quantity):
        self.id = id
        self.quantity = quantity
        self.auctionId = ''

    def createAuction(self):
        roomid=APILink.createAuction(str(self.id),"Seller",self.quantity)
        self.auctionId = roomid
        return roomid

    

