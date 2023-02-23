from SimEngine import *
import Sellers
from Bidder import *
from ReferenceCalculator import *
import random
from DataManagement import *

bidderslist = []
sellerslist = []
seed = None


def readConfig():
    # Reads the config file for seed/numsellers/numbidders
    try:
        config = open("config.txt", "r")
        config.close()

    # If there is no config file, one gets generated and saved with a mathcing checksum
    except:
        config = open('config.txt', "w")
        seed = genSeed()
        numsellers = random.randrange(10,30)
        numrandombidders = random.randrange(5,15)
        ranodomprocent = random.random()
        resourceusage = ranodomprocent
        config.write("seed=" + str(seed) + "\n" + "bidder=" + "number=" + str(
            numrandombidders) + "," + "copy=False" + ":" + "\n" + "seller=" + "number=" + str(
            numsellers) + "," + "randomchainlength=true" + ":" + "\n" + "resourceusage%=" + str(
            int(ranodomprocent * 100)))
        check = (seed * numsellers * numrandombidders)
        config.close()
        return str(check)[0:4]

        # Set the seed for all random numbers generated
    config = open("config.txt", "r")
    text = config.read()
    config.close()
    line = text.split("\n")
    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")
        if rowoflist.find("seed") != -1:
            seed = int(rowoflist.split("=")[1])
            random.seed(seed)

    try:
        if seed == None:
            raise
    except:
        seed = genSeed()
        config = open("config.txt", "a")
        config.write("seed=" + str(seed))
        config.close()

    # reads number of sellers and creates the supply of available material
    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        if rowoflist.find("bidder") != -1:
            numbidder = rowoflist.split(":")[0].split(",")
            for x in numbidder:
                if x.find("number=") != -1:
                    numbidder = int(x.split("number=")[1])

        if rowoflist.find("seller") != -1:
            block = rowoflist.split("seller=")[1]
            numsellers = block.split(":")[0].split(",")
            for x in numsellers:
                if x.find("number=") != -1:
                    numsellers = x.split("number=")[1]
            randomchainlength = block.split(":")[0].split(",")
            for x in randomchainlength:
                if x.find("randomchainlength=") != -1:
                    randomchainlength = x.split("randomchainlength=")[1]
        if rowoflist.find("resourceusage%") != -1:
            resourceusage = int(rowoflist.split("resourceusage%=")[1]) / 100
            """    
            have finished reading the prespecs and will now read real specs
            """
    try:
        numsellers
        block = rowoflist.split(":")[1]
        blocklen = []
        if block.find("->") != -1:
            for x in block.split("->"):
                if x.find("chainlenght") != -1:
                    blocklen.append(x.split("chainlenght=")[1].split(",")[0])
                    block = block.replace(",chainlenght=" + str(x.split("chainlenght=")[1].split(",")[0]), "")
                    block = block.replace("chainlenght=" + str(x.split("chainlenght=")[1].split(",")[0]), "")
                elif x.find("[") != -1 and x.find("]") != -1:
                    blocklen.append(x.count("["))
                else:
                    if randomchainlength == "true":
                        blocklen.append(random.randrange(2, 9))# can specify random range of blocklenght
                    else:
                        blocklen.append(1)
                block = block + "->"
        sumofremainingblocks = 0
        randomblocklengt = []
        for x in range(int(numsellers)-len(blocklen)):
            rng=random.randrange(10,100)
            sumofremainingblocks = sumofremainingblocks + rng
            randomblocklengt.append(rng)
        for x in randomblocklengt:
            blocksize = int((x / sumofremainingblocks) * numbidder)+1
            blocklen.append(blocksize)
            block = block + "->"
        for x in range(int(numsellers)):
            blockatribute = block.split("->")[x]
            seller = Sellers.Sellers(len(sellerslist))
            sellerslist.append(seller)
            headcreated = False
            for i in range(int(blocklen[x])):
                price = None
                supply = None
                discount = None
                try:
                    blockinfo = blockatribute.split("[")[1].split("]")[0].split(",")
                except:
                    blockatribute = blockatribute.strip(",")
                    blockinfo = blockatribute.split(",")
                for place in range(len(blockinfo)):
                    attribute = blockinfo[place]
                    blockatribute = blockatribute.replace("[", "", 1)
                    blockatribute = blockatribute.replace("]", "", 1)
                    if attribute.find("price") != -1:
                        price = int(attribute.split("price=")[1])
                        blockatribute = blockatribute.replace(",price=" + str(price), "")
                        blockatribute = blockatribute.replace("price=" + str(price), "")
                    elif attribute.find("supply") != -1:
                        supply = int(attribute.split("supply=")[1])
                        blockatribute = blockatribute.replace(",supply=" + str(supply), "")
                        blockatribute = blockatribute.replace("supply=" + str(supply), "")
                    elif attribute.find("discount") != -1:
                        discount = int(attribute.split("discount=")[1])
                        blockatribute = blockatribute.replace(",discount=" + str(discount), "")
                        blockatribute = blockatribute.replace("discount=" + str(discount), "")
                if price == None:
                    price = random.randrange(1000, 10000)
                if supply == None:
                    supply = random.randrange(100, 1000)
                if discount == None:
                    discount = random.randrange(0, 100)

                if headcreated:
                    seller.addBlock(price, supply, discount)
                else:
                    seller.genBlock(price, supply, discount)
                    headcreated = True
    except:
        if len(sellerslist) == 0:
            numsellers = genAmountSellers()
            config = open("config.txt", "a")
            config.write("\nseller=" + "number=" + str(numsellers) + "," + "randomchainlength=true" + ":")
            config.close()



    try:
        resourceusage
    except:
        ranodomprocent = random.random()
        resourceusage = ranodomprocent
        config = open("config.txt", "a")
        config.write("\n" + "resourceusage%=" + str(int(ranodomprocent * 100)))
        config.close()



    # calculate the total sum of supply available
    sum = 0
    for sellers in sellerslist:
        blocklist = sellers.LinkOfBlocks.display()
        for block in blocklist:
            sum = sum + int(block.Amount)
    totalbudget = sum * resourceusage

    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        # reads demands for buyers
        if rowoflist.find("bidder") != -1 and rowoflist.find("numrandombidders") == -1:
            bidderprespec = rowoflist.split("bidder=")[1]
            if bidderprespec.find("number") != -1:
                numbidder = bidderprespec.split(":")[0].split(",")
                for x in numbidder:
                    if x.find("number=") != -1:
                        numbidder = int(x.split("number=")[1])
            else:
                numbidder = random.randrange(1, 15)
            copy = bidderprespec.split(":")[0].split(",")
            for x in copy:
                if x.find("copy=") != -1:
                    copy = x.split("copy=")[1]
            """    
            have finished reading the prespecs and will now read real specs
            """
            bidderspec = rowoflist.split(":")[1]
            if bidderspec.find("->") != -1:
                listbidderatribute = bidderspec.split("->")
            else:
                listbidderatribute = []
            while len(listbidderatribute) < int(numbidder):
                listbidderatribute.append("")
            names = []
            amounts = []
            needs = []
            behaviours = []
            marketprices = []
            supply = None
            demand = None
            behaviour = None
            marketprice = None
            sumofsetdemand = 0
            listofzero = []
            for bidderattribute in listbidderatribute:
                if copy != "true":
                    supply = None
                    demand = None
                    behaviour = None
                    marketprice = None
                name = None
                attribute = bidderattribute.split(",")
                for x in attribute:
                    if x.find("supply=") != -1:
                        supply = x.split("supply=")[1]
                        amounts.append(supply)
                        name = 200
                    elif x.find("demand=") != -1:
                        demand = x.split("demand=")[1]
                        needs.append(demand)
                        name = 200
                    elif x.find("behaviour=") != -1:
                        behaviour = x.split("behaviour=")[1]
                        behaviours.append(behaviour)
                        name = 200
                    elif x.find("marketprice=") != -1:
                        marketprice = x.split("marketprice=")[1]
                        marketprices.append(marketprice)
                        name = 200
                if name != None:
                    name = name + len(bidderslist)
                else:
                    name = len(bidderslist)
                names.append(name)
                if supply == None:
                    amounts.append(random.randrange(10, 200))
                if demand == None:
                    needs.append(0)
                if behaviour == None:
                    behaviours.append(Behaviour.randomBehaviour())
                if marketprice == None:
                    marketprices.append(random.randrange(1000, 10000))
            for x in range(len(needs)):
                if needs[x] == 0:
                    listofzero.append(x)
                sumofsetdemand = sumofsetdemand + int(needs[x])
                # generate random procentual usage for each bidder to match the total budget
            procentdemands = []
            sumdemands = 0
            for x in listofzero:
                rng = random.randrange(10, 100)  # can specify range of upper and lower demands here in %
                sumdemands = sumdemands + rng
                procentdemands.append(rng)
            i = 0
            for x in listofzero:
                rng = procentdemands[i]
                procent = rng / (sumdemands)
                budgetuse = procent * (totalbudget - sumofsetdemand)
                needs[x] = budgetuse
                i = i + 1
            for x in range(numbidder):
                name = names[x]
                supply = amounts[x]
                demand = needs[x]
                behaviour = behaviours[x]
                marketprice = marketprices[x]

                # id,supply,needs,behaviour,marketprice,totalbudget,resourceusage
                spentbudget = createBidder(namn=name, amount=supply, needs=demand, behaviour=behaviour,
                                           marketprice=marketprice, budget=totalbudget)
                totalbudget = totalbudget - spentbudget

    if len(bidderslist) == 0:
        numrandombidders = genNumBuyers()
        config = open("config.txt", "a")
        config.write("\n" + "bidder=" + "number=" + str(numrandombidders) + "," + "copy=False" + ":")
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
    for x in range(amountsellers):
        createRandomSeller()
    return amountsellers


def genNumBuyers():
    numbuyers = random.randrange(10, 30)
    for x in range(numbuyers):
        createBidder()
    return numbuyers


# creates bidders from config or random if no value was given
def createBidder(**kwargs):
    try:
        kwargs["budget"]
    except:
        kwargs["budget"] = random.randrange(10, 100)
    try:
        if kwargs["amount"] != None:
            amount = kwargs["amount"]
        else:
            raise
    except:
        amount = random.randrange(10, 200)
    try:
        namn = kwargs["namn"]
    except:
        namn = "Buyer", len(bidderslist)
    try:
        need = Needs(int(kwargs["needs"]), "stenmalm")
        if int(kwargs["budget"]) < 0:
            raise Exception("cant be more demand then supply")
    except:
        if int(kwargs["budget"]) < 0:
            raise Exception("cant be more demand then supply")
        else:
            need = Needs(random.randrange(int(kwargs["budget"] * 0.7), int(kwargs["budget"])), "Stenmalm")
    try:
        marketprice = kwargs["marketprice"]
    except:
        marketprice = random.randrange(1000, 10000)
    try:
        behaviour = kwargs["behaviour"]
    except:
        behaviour = Behaviour.randomBehaviour()

    # id, currentamount, needs, behaviour, marketPrice
    bidderslist.append(Bidder(namn, amount, need, marketprice, behaviour))
    return need.amount

    # creates number of sellers


def createRandomSeller():
    price = random.randrange(1000, 10000)
    amount = random.randrange(100, 1000)
    discount = random.randrange(0, 100)
    seller = Sellers.Sellers(len(sellerslist))
    seller.genBlock(price, amount, discount)
    sellerslist.append(seller)


checksum = readConfig()

sum = 0
for x in bidderslist:
    sum = sum + x.needs.amount
print(sum, "sum of demand")


for x in sellerslist:
    print(x.LinkOfBlocks.display())



sumblocks = 0
sumseller = 0
for x in sellerslist:
    list = x.LinkOfBlocks.display()
    for i in list:
        sumseller = sumseller + i.Amount
        x.quantity = i.Amount
        sumblocks = sumblocks + 1
print(sumseller, "sum of supply")

print(sumblocks)
print(len(bidderslist))
resourceusage = sum / sumseller

# aucitonengine = SimEngine(sellerslist,10,bidderslist)

# DataManagement.dataCollector(seed,sellerslist,bidderslist,resourceusage,sum,sumseller,checksum)
