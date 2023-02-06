class AuctionBlock:
    def __init__(self, Object = None):
        self.Object = Object
        self.Units = None
        self.Price = None
        self.Discount = None
        self.NextBlock = None

    def get_Object(self):
        return self.Object

    def get_amount(self):
        return self.Amount

    def set_amount(self, Amount):
        self.Amount = Amount

    def get_price(self):
        return self.Price

    def set_price(self, Price):
        self.Price = Price

    def get_discount(self):
        return self.Discount

    def set_discount(self, Discount):
        self.Discount = Discount

    def set_nextBlock(self, NextBlock):
        self.NextBlock = NextBlock

class LinkOfBlocks:
    def __init__(self):
        self.head = AuctionBlock()
        self.size = 0   

    def get_size(self):
        return self.size

    def add(self, Object):
        newBlock = AuctionBlock(Object)
        currentBlock = self.head
        while currentBlock.NextBlock != None:
            currentBlock = currentBlock.NextBlock
        currentBlock.NextBlock = newBlock
        self.size += 1

    def display(self):
        Blocks = []
        currentBlock = self.head
        while currentBlock.NextBlock != None:
            currentBlock = currentBlock.NextBlock
            Blocks.append(currentBlock.Object)
        print(Blocks)




