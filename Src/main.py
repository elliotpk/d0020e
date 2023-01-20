import random
import SimEngine
from Bidder import Bidder
from Bidder import Needs
from Bidder import Behaviour

def readConfig():
    global seed
    global numbuyers
    global data
    #Reads the config file for seed/data/numbuyers
    try:
        config = open("config.txt","r")
        text=config.read()
        text.replace("  ","")
        line = text.split("\n")
        for x in line:
            x.strip()
            if x.find("seed")!=-1:
                seed=int(x.strip("seed= "))
                random.seed(seed)
            elif x.find("numbuyers")!=-1:
                numbuyers=int(x.strip("numbuyers= "))
            elif x.find("data")!=-1:
                data=int(x.strip("data= "))
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
            data
        except:
            data=genData()
            config = open("config.txt","a")
            config.write("data="+str(data))
            config.close()
        try:
            numbuyers
        except:
            numbuyers=genNumBuyers()
            config = open("config.txt","a")
            config.write("numbuyers="+str(numbuyers))
            config.close()

        #returns a checksum for comparisons
        check = (seed * data * numbuyers)
        return str(check)[0:4]

    #If there is no config file, one gets generated and saved with a mathcing checksum
    except:
        config = open('config.txt', "w")
        seed=genSeed()
        data=genData()
        numbuyers=genNumBuyers()
        config.write("seed="+str(seed)+"\n""numbuyers="+str(numbuyers)+"\n"+"data="+str(data))
        print("generated indata")
        check = (seed * data * numbuyers)
        return str(check)[0:4]



def genSeed():
    rng = random.randrange(0, 10000)
    random.seed(rng)
    seed=rng
    return seed

def genData():
    data = random.randrange(0, 5000)
    return data

def genNumBuyers():
    numbuyers = random.randrange(0, 100)
    return numbuyers




#main() call on setup, reference, simengine

#setup() setup all

#printseed()

#Graphs()

checksum=readConfig()



Bidders=[]


# id, name, currentamount, needs, behaviour, marketPrice

for x in range(numbuyers):
    Bidders.append("Bidder"+str(x))
    Bidders[x]=Bidder(x,"Namn",random.randint(0, 100),Needs(random.randint(5, 50), "bilar"),Behaviour.A,data)




#SimEngine.printdata("checksum="+str(checksum)+";"+"pris,data,vinnare,id;1,sten,34,#91;420,lera,2,#54") prints
