#DataManagement
import os


class DataManagement:

    def __init__(self):
        self.DataList = None
        self.string = ""
        self.stringlist = []

    #When this function is called, stringlist have all the strings it need
    #to write a CSV-file so it just adds a title to every column and prints it.
    def simulationDone(self):
        self.stringlist.insert(0,"id,user,bid")
        self.stringlist
        self.printdata(testtype="testE")

    #Everytime a row of data is made to a string this function adds it to stringlist
    #and resets the string-variable.
    def addToStringlist(self, string):
        self.stringlist.append(string)
        self.string = ""

    #Recievs a list with data from SimEngine and data from every item becomes one string
    #that will make one row in a csvfile.
    def stringMaker(self, list):
        self.DataList = list

        for item in self.DataList:
            self.string += item["id"] + "," + item["user"] + "," + str(item["top_bid"])
            self.addToStringlist(self.string)

    #Recievs data of different types from main. Just like stringmaker every string represents
    #a row in the becoming csvfile
    def dataCollector(self, seed, sellerslist, bidderslist, resourceusage, sum, sumseller, checksum, rajFairness):

        #Begins vid the header row with tiles for each column
        self.stringlist = ["ID,AuctionID,Quantity,NumOfAuctions," + "Rajafairness=" + str(rajFairness)]
        #Sellerslist contain instances of the seller class.
        #Loop throug all sellers and makes string of relevant data in them
        #and adds the to stringlist
        for seller in sellerslist:
            for i in range(len(seller.auctionId)):
                self.string = str(seller.id) + "," + str(seller.auctionId[i]) + "," + str(seller.quantity[i]) + str(seller.LinkOfBlocks.size)
                self.addToStringlist(self.string)
                self.string = ""
        #self.mktxtfl(seed)
        #When the loop is done printdata is called to make a csvfile
        self.printdata(testtype = "testJseller")
        
        #Begins vid the header row with tiles for each column
        self.stringlist = ["ID,Needs,Marketprice,Behaviour"]
        #bidderslist contain instances of the bidder class.
        #Loop throug all bidders and makes string of relevant data in them
        #and adds the to stringlist
        for bidder in bidderslist:
            self.string = str(bidder.id) + "," + str(bidder.needs.amount) + "," + str(bidder.marketPrice) + "," + str(bidder.behaviour["behaviour"])
            self.addToStringlist(self.string)
            self.string = ""
        #self.mktxtfl(seed)
        #Like above an new csvfile is made
        self.printdata(testtype = "testJbidder")


    #Prints the results into a csv file and labels the different runs into a new csv file
    def printdata(self, testtype):
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

    #Function to plot graphs with information. Not invoked because its not finished
    """
    def graphPloter(self, csvfile):

        datafile = pd.read_csv(csvfile)

        graphs = datafile.plot(x='Bidders', y=['bidder1', 'bidder2','bidder3','bidder4'])
        graphs.set_ylabel('bids (USD)')
        plt.show()
    """

    def mktxtfl(self, seed, testid):

     
        if (os.path.exists(str(seed)+'.txt')):
            mktxt = open(str(seed)+'.txt','w')
            mktxt.write("\n\n")
            for string in self.stringlist:
                for row in string.split(' '):
                    mktxt.write(row+"\n")
            mktxt.write("\n\n")
        else:
            mktxt = open(str(seed)+'.txt','w')
            for string in self.stringlist:
                for row in string.split(' '):
                    mktxt.write(row+"\n")
            mktxt.close()


        
    

