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
    # Reads the config file if it exists
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
        endthreshold = 2
        slotsize = 2
        config.write("seed=" + str(seed) + "\n" + "bidder=" + "number=" + str(
            numrandombidders) + "," + "copy=False" + ":" + "\n" + "seller=" + "number=" + str(
            numsellers) + "," + "randomchainlength=true" + ":" + "\n" + "resourceusage%=" + str(
            int(ranodomprocent * 100))+"\n"+"endthreshold = 2"+"\n"+"slotsize = 2")
        check = (seed * numsellers * numrandombidders)
        config.close()
        return str(check)[0:4],slotsize,endthreshold

        # Find if there is a seed in the config
    config = open("config.txt", "r")
    text = config.read()
    config.close()
    line = text.split("\n")
    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")
        if rowoflist.find("seed") != -1:
            seed = int(rowoflist.split("seed=")[1])
            random.seed(seed)

        # if there is no seed one gets generated
    try:
        if seed == None:
            raise
    except:
        seed = genSeed()
        config = open("config.txt", "a")
        config.write("seed=" + str(seed))
        config.close()

    # reads number of sellers and generates the supply of available material
    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        # read number of bidders
        if rowoflist.find("bidder") != -1:
            numbidder = rowoflist.split(":")[0].split(",")
            for x in numbidder:
                if x.find("number=") != -1:
                    numbidder = int(x.split("number=")[1])

        # read number of sellers, and if randomchainlenght is true
        if rowoflist.find("seller") != -1:
            block = rowoflist.split("seller=")[1]
            numsellers = block.split(":")[0].split(",")
            for x in numsellers:
                if x.find("number=") != -1:
                    numsellers = x.split("number=")[1]
                if x.find("randomchainlength=") != -1:
                    randomchainlength = x.split("randomchainlength=")[1]

        # reads resourceusage%, slotsize, endthreshold
        if rowoflist.find("resourceusage%") != -1:
            resourceusage = int(rowoflist.split("resourceusage%=")[1]) / 100

        if rowoflist.find("slotsize") != -1:
            slotsize = int(rowoflist.split("slotsize=")[1])

        if rowoflist.find("endthreshold") != -1:
            endthreshold = int(rowoflist.split("endthreshold=")[1])
            """    
            have finished reading the prespecs and will now read real seller specs
            """
    # Generates the data for every seller
    try:
        # Reads the specified amount of blocks
        numsellers
        block = block.split(":")[1]
        blocklen = []
        for x in block.split("->"):
            if x.find("chainlength") != -1:
                if x.find(",") != -1:
                    blocklen.append(x.split("chainlength=")[1].split(",")[0])
                else:
                    blocklen.append(x.split("chainlength=")[1])
            elif x.find("[") != -1 and x.find("]") != -1:
                blocklen.append(x.count("["))
            else:
                try:
                    if randomchainlength == "true":
                        if len(block.split("->")) != 1:
                            blocklen.append("replace")
                    else:
                        raise
                except:
                    blocklen.append("replace")

        # Generates the missing blocks to match the number of buyers
        sumofremainingblocks = 0
        randomblocklengt = []
        listofreplace = []
        loop = 0
        for x in range(len(blocklen)):
            if blocklen[x]== "replace":
                listofreplace.append(x)
        for x in range(int(numsellers)+len(listofreplace)-len(blocklen)):
            rng=random.randrange(10,100)
            sumofremainingblocks = sumofremainingblocks + rng
            randomblocklengt.append(rng)
        for x in randomblocklengt:
            try:
                if randomchainlength == "true":
                    factor = random.uniform(1,4)
                else:
                    raise
            except:
                factor = 1
            blocksize = 1+int((x / sumofremainingblocks) * numbidder*factor)
            try:
                listofreplace[loop]
                blocklen[listofreplace[loop]] = blocksize
            except:
                blocklen.append(blocksize)
            loop += 1
            block = block + "->"

        #generates /reads the information in each block
        for x in range(int(numsellers)):
            blockatribute = block.split("->")[x]
            seller = Sellers.Sellers(len(sellerslist))
            sellerslist.append(seller)
            headcreated = False
            discount = None
            for i in range(int(blocklen[x])):
                price = None
                supply = None
                discountbool = True
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
                        discountbool = False
                        discount = int(attribute.split("discount=")[1])
                        blockatribute = blockatribute.replace(",discount=" + str(discount), "")
                        blockatribute = blockatribute.replace("discount=" + str(discount), "")
                if price == None:
                    price = random.randrange(1000, 10000)
                if supply == None:
                    supply = random.randrange(100, 1000)
                if discountbool:
                    if i > 0:
                        discount = int((discount + random.randrange(1,10))/(i+1))
                    else:
                        discount = random.randrange(0, 10)

                if headcreated:
                    seller.addBlock(price, supply, discount)
                else:
                    seller.genBlock(price, supply, discount)
                    headcreated = True

    #generates new sellers if none existed in the config
    except Exception as e:
        if len(sellerslist) == 0:
            numsellers = genAmountSellers()
            config = open("config.txt", "a")
            config.write("\nseller=" + "number=" + str(numsellers) + "," + "randomchainlength=true" + ":")
            config.close()

    #check if resourceusage, slotsize, endthreshold exists
    try:
        resourceusage
    except:
        ranodomprocent = random.random()
        resourceusage = ranodomprocent
        config = open("config.txt", "a")
        config.write("\n" + "resourceusage%=" + str(int(ranodomprocent * 100)))
        config.close()

    try:
        if slotsize == None:
            raise
    except:
        slotsize = 2
        config = open("config.txt", "a")
        config.write("\n" + "slotsize=" + str(slotsize))
        config.close()

    try:
        if endthreshold == None:
            raise
    except:
        endthreshold = 2
        config = open("config.txt", "a")
        config.write("\n" + "endthreshold=" + str(endthreshold))
        config.close()

    # calculate the total sum of supply available
    sum = 0
    for sellers in sellerslist:
        blocklist = sellers.LinkOfBlocks.display()
        for block in blocklist:
            sum = sum + int(block.Amount)
    totalbudget = sum * resourceusage
    if sum < totalbudget:       #checks if there is more demand then supply
        raise Exception("Can't be more demand then supply")

    for rowoflist in line:
        rowoflist = rowoflist.replace(" ", "")

        # reads demands for buyers
        if rowoflist.find("bidder") != -1:
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
            needs = []
            behaviours = []
            marketprices = []
            demand = None
            behaviour = None
            marketprice = None
            sumofsetdemand = 0
            listofzero = []
            for bidderattribute in listbidderatribute:
                if copy != "true":
                    demand = None
                    behaviour = None
                    marketprice = None
                name = None
                attribute = bidderattribute.split(",")
                for x in attribute:
                    if x.find("demand=") != -1:
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
                    name ="Buyer"+ str(name + len(names))
                else:
                    name ="Buyer"+ str(len(names))
                names.append(name)

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
                maxround=0
                for i in sellerslist:
                    list = i.LinkOfBlocks.display()
                    maxround = maxround+len(list)
                name = names[x]
                demand = needs[x]
                behaviour = behaviours[x]
                marketprice = marketprices[x]

                # id,supply,needs,behaviour,marketprice,totalbudget,resourceusage
                spentbudget = createBidder(namn=name, maxrounds=maxround/slotsize, needs=demand, behaviour=behaviour,
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
    return str(check)[0:4],slotsize,endthreshold


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
        if kwargs["maxrounds"] != None:
            maxrounds = kwargs["maxrounds"]
        else:
            raise
    except:
        maxrounds = random.randrange(1,20)
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
        kwargs["behaviour"]
        behaviour = Behaviour.getBehaviour(kwargs["behaviour"])
    except Exception as e:
        print(e)
        behaviour = Behaviour.randomBehaviour()

    # id, currentamount, needs, behaviour, marketPrice
    bidderslist.append(Bidder(namn, need, math.ceil(maxrounds), behaviour))
    return need.amount

    # creates random sellers
def createRandomSeller():
    price = random.randrange(1000, 10000)
    amount = random.randrange(100, 1000)
    discount = random.randrange(0, 100)
    seller = Sellers.Sellers(len(sellerslist))
    seller.genBlock(price, amount, discount)
    sellerslist.append(seller)

def callOnReferenceCalculator():
    fairness, marketprice = referenceCalculator(sellerslist, bidderslist)
    if fairness == -1: print("No valid combinations were found")
    return fairness, marketprice

def uppdateBidder(marketprice):
    for x in bidderslist:
        x.setMarketprice(marketprice)

def uppdateSeller():
    sum = 0
    for x in bidderslist:
        sum = sum + x.needs.amount

    sumblocks = 0
    sumofsopply = 0
    for x in sellerslist:
        sumseller = 0
        list = x.LinkOfBlocks.display()
        for i in list:
            sumofsopply = sumofsopply + i.Amount
            sumseller = sumseller + i.Amount
            x.quantity.append(i.Amount)
            sumblocks = sumblocks + 1
    resourceusage = (sum/sumseller)
    return resourceusage,sumseller,sum


checksum,slotsize,endthreshold = readConfig()
#starts the other prosseces

fairness,marketprice=callOnReferenceCalculator()
uppdateBidder(marketprice)
resourceusage,sumseller,sum = uppdateSeller()

aucitonengine = SimEngine(sellerslist,bidderslist,slotsize,endthreshold)
aucitonengine.simStart()

DataManagement().dataCollector(seed, sellerslist, bidderslist, resourceusage, sum, sumseller, checksum,fairness)
