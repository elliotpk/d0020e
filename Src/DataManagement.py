#DataManagement

class DataManagement:

    def __init__(self):
        #different types of relevant data
        self.AuctionWinner = None
        self.BiddingHistory = None
        self.Price = None
        self.ObjectType = None
        self.Amount = None
        self.Discount = None
        self.DataList = [
                    "AuctionWinner",
                    "BiddingHistory",
                    "Price",
                    "ObjectType",
                    "Amount",
                    "Discount",
                    "DataList"] #Hard coded list just for demonstration of the idea of how it will work


    #Function to collect relevant data from API and other classes
    def dataCollector(self):

    #def get_AuctionWinner(self):
        self.AuctionWinner = "AuctionWinner" #Theese are supposed to call other classes to collect data but for now i'm just putting strings into the variables to be able to test the function
        self.DataList.append(self.AuctionWinner)

    #def getBiddingHistory(self):
        self.BiddingHistory = "BiddingHistory"
        self.DataList.append(self.BiddingHistory)

    #def getPrice(self):
        self.Price = "Price"
        self.DataList.append(self.Price)

    #def get_ObjectType(self):
        self.ObjectType = "ObjectType"
        self.DataList.append(self.ObjectType)

    #def get_Amount(self):
        self.Amount = "Amount"
        self.DataList.append(self.Amount)

    #def get_Discount(self):
        self.Discount = "Discount"
        self.DataList.append(self.Discount)


    #Function to choose output based on user desire

    def dataOutput(self, DesiredData):

        self.DesiredData = DesiredData
        DataOutputList = []

        for i in self.DesiredData:
            DataOutputList.append(self.DataList[i])
        return DataOutputList

    def userTest(self):

        DesiredData = []

        print("Enter the number of datatypes to display\n\n"

        "0. Done.\n"
        "1. AuctionWinner\n"
        "2. BiddingHistory\n"
        "3. Price\n"
        "4. ObjectType\n"
        "5. Amount\n"
        "6. Discount\n"
        "7. DataList\n\n"  )

        while True:
        
            i = input("Enter number of datatypes to display: ")

            if int(i) != 0:
                DesiredData.append(int(i))
            else:
                return print(self.dataOutput(DesiredData))
                


#D = DataManagement()

#D.userTest()