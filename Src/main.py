import random
import SimEngine
from Sellers import Sellers
from Sellers import Block
from Bidder import Bidder
from Bidder import Needs
from Bidder import Behaviour
global bidderslist
bidderslist = []
global sellerslist
sellerslist = []
def readConfig():
    #Reads the config file for seed/numsellers/numrandombidders
    try:
        config = open("config.txt","r")
        text=config.read()
        line = text.split("\n")
        for rowoflist in line:
            rowoflist=rowoflist.replace(" ","")
            if rowoflist.find("seed")!=-1:
                seed=int(rowoflist.split("=")[1])
                random.seed(seed)

            #reads number of random bidders
            elif rowoflist.find("numrandombidders")!=-1:
                numrandombidders=rowoflist.split("=")
                numrandombidders=int(numrandombidders[1])
                if int(numrandombidders) < 1:
                    continue
                for x in range(numrandombidders):
                    createBidder()

            #reads number of sellers
            elif rowoflist.find("numsellers")!=-1:
                numsellers=rowoflist.split("=")
                number=int(numsellers[1])
                for x in range(number):
                    createSeller()

            #reads demands for buyers
            elif rowoflist.find("bidder") != -1 and rowoflist.find("numrandombidders") == -1:
                rowoflist=rowoflist.split(",")
                namn=None
                amount=None
                need=None
                behaviour=None
                marketprice=None
                for i in range(len(rowoflist)):
                    if rowoflist[i].find("bidder")!=-1:
                        rowoflist[i]=rowoflist[i].split("bidder")[1]
                        namn=rowoflist[i]
                    elif rowoflist[i].find("amount")!=-1:
                        rowoflist[i]=rowoflist[i].split("=")[1]
                        amount=rowoflist[i]
                    elif rowoflist[i].find("need")!=-1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        need=rowoflist[i]
                    elif rowoflist[i].find("behaviour")!=-1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        behaviour=rowoflist[i]
                    elif rowoflist[i].find("marketprice")!=-1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        marketprice = rowoflist[i]
                    #id,amount,needs,behaviour,marketprice
                createBidder(namn=namn,amount=amount,needs=need,behaviour=behaviour,marketprice=marketprice)




        config.close()

        #If somtihing is missing then only that gets generated
        try:
            seed
        except:
            seed=genSeed()
            config = open("config.txt","a")
            config.write("seed="+str(seed))
            config.close()
        try:
            numsellers
        except:
            numsellers=genRandomAmountSellers()
            config = open("config.txt","a")
            config.write("numsellers="+str(numsellers))
            config.close()
        try:
            numrandombidders
        except:
            numrandombidders=genNumBuyers()
            config = open("config.txt","a")
            config.write("numrandombidders="+str(numrandombidders))
            config.close()

        #returns a checksum for comparisons
        check = (seed * numsellers * numrandombidders)
        return str(check)[0:4]

    #If there is no config file, one gets generated and saved with a mathcing checksum
    except:
        config = open('config.txt', "w")
        seed=genSeed()
        numrandomsellers=genRandomAmountSellers()
        numrandombidders=genNumBuyers()
        config.write("seed="+str(seed)+"\n""numrandombidders="+str(numrandombidders)+"\n"+"numrandomsellers="+str(numrandomsellers))
        check = (seed * numrandomsellers * numrandombidders)
        return str(check)[0:4]




def genSeed():
    rng = random.randrange(0, 10000)
    random.seed(rng)
    seed=rng
    return seed

def genRandomAmountSellers():
    #amountsellers = random.randrange(0, 8)
    amountsellers = 1
    return amountsellers

def genNumBuyers():
    numbuyers = random.randrange(0, 100)
    return numbuyers




#main() call on setup, reference, simengine

#setup() setup all

#printseed()

#Graphs()








#creates bidders from config or random if no value was given
def createBidder(**kwargs):
    try:
        if kwargs["namn"] != None:
            namn = kwargs["namn"]
        else:
            raise
    except:
        namn=len(bidderslist)
    try:
        if kwargs["amount"] != None:
            amount = kwargs["amount"]
        else:
            raise
    except:
        amount=random.randrange(10,200)
    try:
        if kwargs["needs"] != None:
            need = kwargs["needs"]
        else:
            raise
    except:
        need=Needs(random.randrange(10,200),"Stenmalm")
    try:
        if kwargs["marketprice"] != None:
            marketprice = kwargs["marketprice"]
        else:
            raise
    except:
        marketprice = random.randrange(1000, 10000)
    try:
        if kwargs["behaviour"] != None:
            behaviour = kwargs["behaviour"]
        else:
            raise
    except:
        #behaviour=bihaviour.getRandomBehaviour
        i=None
    # id, currentamount, needs, behaviour, marketPrice
    bidderslist.append(Bidder(namn,amount,need,marketprice,Behaviour.A))

    #creates number of sellers
def createSeller():
    sellerslist.append(Sellers(len(sellerslist)))



"""   
while next != None:

    print("Block nr "+ str(i)+" price "+str(next.price)+", Amount "+str(next.amount))
    next = next.nextblock
    i = i +1
"""
#SimEngine.printdata("checksum="+str(checksum)+";"+"pris,data,vinnare,id;1,sten,34,#91;420,lera,2,#54") prints



checksum=readConfig()