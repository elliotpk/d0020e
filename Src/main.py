import random
import SimEngine
import Sellers
from Bidder import *
from ReferenceCalculator import *

global bidderslist
bidderslist = []
global sellerslist
sellerslist = []


def readConfig():
    # Reads the config file for seed/numsellers/numrandombidders
    try:
        config = open("config.txt", "r")
        text = config.read()
        config.close()
        line = text.split("\n")

    # If there is no config file, one gets generated and saved with a mathcing checksum
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
            seller = Sellers.Sellers(len(sellerslist))
            headcreated = False
            sellerslist.append(seller)
            block = rowoflist.split("seller=")[1]
            if block.find("->"):
                listblockatribute = block.split("->")
            else:
                print("no ->")
                listblockatribute = block
            for i in range(len(listblockatribute)):
                price = None
                amount = None
                discount = None
                blockatribute = listblockatribute[i].split(",")
                for attribute in blockatribute:
                    if attribute.find("price") != -1:
                        price = int(attribute.split("=")[1])
                    elif attribute.find("amount") != -1:
                        amount = int(attribute.split("=")[1])
                    elif attribute.find("discount") != -1:
                        discount = int(attribute.split("=")[1])
                if price == None:
                    price = random.randrange(1000, 10000)
                if amount == None:
                    amount = random.randrange(1, 100)
                if discount == None:
                    discount = random.randrange(0, 100)

                if headcreated:
                    seller.addBlock(price, amount, discount)
                else:
                    seller.genBlock(price, amount, discount)
                    headcreated = True

    if len(sellerslist) == 0:
        numsellers = genAmountSellers()
        config = open("config.txt", "a")
        config.write("\nnumrandomsellers=" + str(numsellers))
        config.close()

    sum = 0
    for sellers in sellerslist:
        blocklist = sellers.LinkOfBlocks.display()
        for block in blocklist:
            sum = sum + int(block.Amount)
    budget = sum
    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        # reads demands for buyers
        if rowoflist.find("bidder") != -1 and rowoflist.find("numrandombidders") == -1:
            rowoflist = rowoflist.split(",")
            namn = None
            amount = None
            need = None
            behaviour = None
            marketprice = None
            for i in range(len(rowoflist)):
                print(rowoflist[i])
                namn = len(bidderslist) + 200
                rowoflist[i] = rowoflist[i].split("bidder=")[1]
                print(rowoflist[i])
                if rowoflist[i].find("amount=") != -1:
                    rowoflist[i] = rowoflist[i].split("amount=")[1]
                    amount = rowoflist[i]
                elif rowoflist[i].find("need=") != -1:
                    rowoflist[i] = rowoflist[i].split("need=")[1]
                    need = rowoflist[i]
                elif rowoflist[i].find("behaviour=") != -1:
                    rowoflist[i] = rowoflist[i].split("behaviour=")[1]
                    behaviour = rowoflist[i]
                elif rowoflist[i].find("marketprice=") != -1:
                    rowoflist[i] = rowoflist[i].split("marketprice=")[1]
                    marketprice = rowoflist[i]
                # id,amount,needs,behaviour,marketprice
            print(namn, amount, need, behaviour, marketprice, budget)
            newBudget = createBidder(namn=namn, amount=amount, needs=need, behaviour=behaviour,
                                     marketprice=marketprice, budget=budget)
            print(newBudget)
            budget = newBudget

    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        # reads number of random bidders
        if rowoflist.find("numrandombidders") != -1:
            numrandombidders = rowoflist.split("=")
            numrandombidders = int(numrandombidders[1])
            if int(numrandombidders) > 0:
                for x in range(numrandombidders):
                    print(budget)
                    newBudget = createBidder(budget=budget)
                    budget = newBudget

    if len(bidderslist) == 0:
        numrandombidders = genNumBuyers()
        config = open("config.txt", "a")
        config.write("\n"+"numrandombidders=" + str(numrandombidders))
        config.close()

    # returns a checksum for comparisons
    numsellers = len(sellerslist)
    numbuyers = len(bidderslist)
    check = (seed * numsellers * numbuyers)
    return str(check)[0:4]




def genSeed():
    rng = random.randrange(0, 10000)
    random.seed(rng)
    return rng


def genAmountSellers():
    amountsellers = random.randrange(5, 15)
    for x in range(amountsellers - 1):
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
        if kwargs["budget"] == None:
            raise
    except:
        kwargs["budget"] = random.randrange(0, 100)
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
        print(kwargs["needs"])
        if kwargs["needs"] != None:
            need = kwargs["needs"]
        else:
            raise
    except:
        if int(kwargs["budget"]) < 10:
            raise Exception("cant be more demand then supply")
        else:
            need = Needs(random.randrange(10, int(kwargs["budget"])), "Stenmalm")
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
            print("cant be more demand then supply")
            raise Exception("cant be more demand then supply")
    except:
        behaviour = Behaviour.randomBehaviour()
    if int(kwargs["budget"]) - need.amount < 0:
        raise ["cant be more demand then supply"]

    newBudget = int(kwargs["budget"]) - int(need.amount)

    # id, currentamount, needs, behaviour, marketPrice
    bidderslist.append(Bidder(namn, amount, need, marketprice, behaviour))
    return newBudget

    # creates number of sellers


def createRandomSeller():
    price = random.randrange(1000, 10000)
    amount = random.randrange(1, 100)
    discount = random.randrange(0, 100)
    seller = Sellers.Sellers(len(sellerslist))
    seller.genBlock(price, amount, discount)
    sellerslist.append(seller)


# SimEngine.printdata("checksum="+str(checksum)+";"+"pris,data,vinnare,id;1,sten,34,#91;420,lera,2,#54") prints
checksum = readConfig()
sum = 0
for x in sellerslist:
    list = x.LinkOfBlocks.display()
    for i in list:
        sum = sum + i.Amount
print(sum)
