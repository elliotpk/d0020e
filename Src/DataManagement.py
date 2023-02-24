#DataManagement
import csv
import os


class DataManagement:

    def __init__(self):
        self.DataList = None
        self.string = ""
        self.stringlist = []
        self.finished = False


    def simulationDone(self):
        self.finished = True

    def temp(self, string):
        self.stringlist.append(string)
        self.string = ""

    def stringMaker(self, list):
        self.DataList = list
        self.stringlist = ["id,quantity,user,top_bid"]

        for item in self.DataList:
            self.string += item["id"] + "," + str(item["quantity"]) + "," + item["user"] + "," + str(item["top_bid"])
            self.temp(self.string)
        #while self.finished:
            #self.printdata()
        self.printdata(testtype = "testE")

    def dataCollector(self, seed, sellerslist, bidderslist, resourceusage, sum, sumseller, checksum):
        
        self.stringlist = [str(seed) + "," + str(sellerslist) + "," + str(bidderslist) + "," + str(resourceusage) + "," + str(sum) + "," + str(sumseller) + "," + str(sumseller) + "," + str(checksum)]
        self.string = seed + "," + str(sellerslist) + "," + str(bidderslist) + "," + resourceusage + "," + str(sum) + "," + str(sumseller) + "," + str(sumseller) + "," + str(checksum)
        self.temp(self.string)
        self.printdata(testtype = "testJ")
        self.stringlist = []

        for item in sellerslist:
            self.string = str(item)
            self.temp(self.string)
            self.string = ""

        print(self.stringlist)
        self.printdata(testtype = "testJseller")
        self.stringlist = []

        for item in bidderslist:
            self.string = str(item)
            self.temp(self.string)
            self.string = ""

        print(self.stringlist)
        self.printdata(testtype = "testJbidder")
        self.stringlist = []

        #for item in bidder


    def printdata(self, testtype):
        #spara data före print
        #prints the results into a csv file and labels the different runs into a new csv file
        testnr = 0
        while (os.path.exists(testtype+str(testnr)+'.csv')):
            testnr=testnr+1
        print(testnr)
        mkcsv = open(testtype+str(testnr)+'.csv','w')
        for string in self.stringlist:
            for row in string.split(' '):
                mkcsv.write(row+"\n")
        mkcsv.close()
        self.stringlist = []

    """"
    pris,data,vinnare,id
    1,sten,34,#91
    420,lera,2,#54
    """
    #print(Api.data) print to csv-file

    def testOutJ(self):

        self.seed = "Exempel"
        self.sellerslist = ["Hubert", "Bart", "Jakob", "Kasper"]
        self.bidderslist = ["Kenneth", "Per", "Olof", "Eskil"]
        self.resourceusage = "0.3"
        self.sum = 1000
        self.sumseller = 7000
        self.checksum = 2500

        self.dataCollector(self.seed, self.sellerslist, self.bidderslist, self.resourceusage, self.sum, self.sumseller, self.checksum)

    
    def testOutE(self):

        auctionId = "100001"
        quantity = 5
        topBid = {'user' : 1, 'value' : 2000}
        auctionId1 = "100002"
        quantity1 = 7
        topBid1 = {'user' : 2, 'value' : 3000}        
        auctionId2 = "100003"
        quantity2 = 1
        topBid2 = {'user' : 3, 'value' : 4000}        
        auctionId3 = "100004"
        quantity3 = 14
        topBid3 = {'user' : 4, 'value' : 5000}        
        auctionId4 = "100005"
        quantity4 = 20
        topBid4 = {'user' : 5, 'value' : 6000}


        list = [{'id' : auctionId, 'quantity' : quantity, 'user': "Cristian" , 'top_bid' : 500},
                {'id' : auctionId1, 'quantity' : quantity1, 'user': "Edvin" , 'top_bid' : 3500},
                {'id' : auctionId2, 'quantity' : quantity2, 'user': "Johanna" , 'top_bid' : 4300},
                {'id' : auctionId3, 'quantity' : quantity3, 'user': "Gry" , 'top_bid' : 15300},
                {'id' : auctionId4, 'quantity' : quantity4, 'user': "Edward" , 'top_bid' : 1300}]

        self.stringMaker(list)
       
#D = DataManagement()

#D.testOutE()


