from SimEngine import SimEngine
from Bidder import Bidder
from Sellers import Sellers
import random
from Behaviour import randomBehaviour

sellerlist = []
for i in range(4):
    sellerlist.append(Sellers(i, random.randint(100, 500)))
    sellerlist[i].createAuction()

buyerlist = []
for i in range(3):
    buyerlist.append(Bidder('Buyer'+str(i), 500, random.randint(200, 300), 50, randomBehaviour()))

sim =SimEngine(sellerlist, buyerlist)
sim.simStart()


