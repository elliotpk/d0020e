import random
import SimEngine
import Sellers
import Bidder

global bidderslist
bidderslist = []
global sellerslist
sellerslist = []


def readConfig():
    # Reads the config file for seed/numsellers/numrandombidders
    #try:
        config = open("config.txt", "r")
        text = config.read()
        config.close()
        line = text.split("\n")

        # Set the seed for all random numbers generated
        for rowoflist in line:
            rowoflist = rowoflist.replace(" ", "")
            if rowoflist.find("seed") != -1:
                seed = int(rowoflist.split("=")[1])
                random.seed(seed)


        try:
            seed
        except:
            seed = genSeed()
            config = open("config.txt", "a")
            config.write("seed=" + str(seed))
            config.close()

        # reads number of sellers and creates the amount of available material
        for rowoflist in line:
            rowoflist = rowoflist.replace(" ", "")
            if rowoflist.find("numrandomseller") != -1:
                numsellers = rowoflist.split("=")
                numsellers = numsellers[1]
                if int(numsellers) > 0:
                    for x in range(int(numsellers)):
                        createRandomSeller()

            elif rowoflist.find("seller") != -1 and rowoflist.find("numrandomseller") == -1:
                seller=Sellers.Sellers(len(sellerslist))
                headcreated = False
                sellerslist.append(seller)
                block = rowoflist.split("seller=")[1]
                if block.find("->"):
                    listblockatribute=block.split("->")
                else:
                    print("no ->")
                    listblockatribute=block
                for i in range(len(listblockatribute)):
                    blockatribute = listblockatribute[i].split(",")
                    for atrtibute in blockatribute:
                        if atrtibute.find("price")!=-1:
                            price=atrtibute.split("=")[1]
                        elif atrtibute.find("amount")!=-1:
                            amount=atrtibute.split("=")[1]
                        elif atrtibute.find("discount")!=-1:
                            discount=atrtibute.split("=")[1]
                    try:
                        price
                    except:
                        price = random.randrange(1000, 10000)
                    try:
                        amount
                    except:
                        amount = random.randrange(1, 100)
                    try:
                        discount
                    except:
                        discount = random.randrange(0,100)

                    if headcreated:
                        seller.addBlock(price,amount,discount)
                    else:
                        seller.genBlock(price,amount,discount)
                        headcreated = True

        if len(sellerslist) == 0:
            numsellers = genAmountSellers()
            config = open("config.txt", "a")
            config.write("numrandomsellers=" + str(numsellers)+"\n")
            config.close()

        sum=0
        for sellers in sellerslist:
            blocklist=sellers.LinkOfBlocks.display()
            for block in blocklist:
                sum=sum+int(block.Amount)
        print(sum)
        for rowoflist in line:
            rowoflist = rowoflist.replace(" ", "")

            # reads number of random bidders
            if rowoflist.find("numrandombidders") != -1:
                numrandombidders = rowoflist.split("=")
                numrandombidders = int(numrandombidders[1])
                if int(numrandombidders) > 0:
                    for x in range(numrandombidders):
                        createBidder()



            # reads demands for buyers
            elif rowoflist.find("bidder") != -1 and rowoflist.find("numrandombidders") == -1:
                rowoflist = rowoflist.split(",")
                namn = None
                amount = None
                need = None
                behaviour = None
                marketprice = None
                for i in range(len(rowoflist)):
                    if rowoflist[i].find("bidder") != -1:
                        rowoflist[i] = rowoflist[i].split("bidder")[1]
                        namn = rowoflist[i]
                    elif rowoflist[i].find("amount") != -1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        amount = rowoflist[i]
                    elif rowoflist[i].find("need") != -1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        need = rowoflist[i]
                    elif rowoflist[i].find("behaviour") != -1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        behaviour = rowoflist[i]
                    elif rowoflist[i].find("marketprice") != -1:
                        rowoflist[i] = rowoflist[i].split("=")[1]
                        marketprice = rowoflist[i]
                    # id,amount,needs,behaviour,marketprice
                createBidder(namn=namn, amount=amount, needs=need, behaviour=behaviour, marketprice=marketprice)



        if len(bidderslist)==0:
            numrandombidders = genNumBuyers()
            config = open("config.txt", "a")
            config.write("numrandombidders=" + str(numrandombidders)+"\n")
            config.close()

        # returns a checksum for comparisons
        numsellers=len(sellerslist)
        numbuyers=len(bidderslist)
        check = (seed * numsellers * numbuyers)
        return str(check)[0:4]

    # If there is no config file, one gets generated and saved with a mathcing checksum
"""
    except:
        config = open('config.txt', "w")
        seed = genSeed()
        numrandomsellers = genAmountSellers()
        numrandombidders = genNumBuyers()
        config.write(
            "seed=" + str(seed) + "\n""numrandombidders=" + str(numrandombidders) + "\n" + "numrandomsellers=" + str(
                numrandomsellers))
        check = (seed * numrandomsellers * numrandombidders)
        return str(check)[0:4]

"""
def genSeed():
    rng = random.randrange(0, 10000)
    random.seed(rng)
    return rng


def genAmountSellers():
    # amountsellers = random.randrange(0, 8)
    amountsellers = 1
    for x in range(amountsellers-1):
        createRandomSeller()
    return amountsellers


def genNumBuyers():
    numbuyers = random.randrange(0, 100)
    createBidder()
    return numbuyers


# main() call on setup, reference, simengine

# setup() setup all

# printseed()

# Graphs()


# creates bidders from config or random if no value was given
def createBidder(**kwargs):
    try:
        if kwargs["namn"] != None:
            namn = kwargs["namn"]
        else:
            raise
    except:
        namn = len(bidderslist)
    try:
        if kwargs["amount"] != None:
            amount = kwargs["amount"]
        else:
            raise
    except:
        amount = random.randrange(10, 200)
    try:
        if kwargs["needs"] != None:
            need = kwargs["needs"]
        else:
            raise
    except:
        need = Bidder.Needs(random.randrange(10, 200), "Stenmalm")
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
        behaviour = Bidder.Behaviour.randomBehaviour()
        i = None
    # id, currentamount, needs, behaviour, marketPrice
    bidderslist.append(Bidder.Bidder(namn, amount, need, marketprice, behaviour))
    # creates number of sellers



def createRandomSeller():
        price = random.randrange(1000, 10000)
        amount = random.randrange(1, 100)
        discount = random.randrange(0,100)
        seller = Sellers.Sellers(len(sellerslist))
        seller.genBlock(price, amount, discount)
        sellerslist.append(seller)
# SimEngine.printdata("checksum="+str(checksum)+";"+"pris,data,vinnare,id;1,sten,34,#91;420,lera,2,#54") prints


checksum = readConfig()