class AuctionBlock:
    #
    def __init__(self):
        self.Object = None
        self.Units = None
        self.Price = None
        self.Discount = None
        self.NextBlock = None
        self.prevBlock = None

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

    def set_prevBlock(self, prevBlock):
        self.prevBlock = prevBlock

    def prev(self):
        return self.prevBlock

    def next(self):
        return self.NextBlock

    def __repr__(self) -> str:
        return self.Object


class LinkOfBlocks:
    def __init__(self):
        self.head = AuctionBlock()
        self.size = 0

    def get_size(self):
        return self.size

    def add(self, Object):
        newBlock = Object
        currentBlock = self.head
        while currentBlock.NextBlock != None:
            currentBlock = currentBlock.NextBlock
        currentBlock.NextBlock = newBlock
        self.size += 1

    def display(self):
        Blocks = []
        currentBlock = self.head
        Blocks.append(currentBlock)
        while currentBlock.NextBlock != None:
            currentBlock = currentBlock.NextBlock
            Blocks.append(currentBlock)
        return Blocks