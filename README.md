# Simulation environment for demand-supply matching

This project aims to provide a simulation environment and matchmaking for demand-supply matching.

## How to run:

The simulator is dependant on a fork of the Negotiation Engine API: https://github.com/elliotpk/NegotiationEngine to run the simulations, you will also need to setup a mongoDB database. For this system we use "API PILOT 1" from the API, make sure to set your database in db.py, "client = MongoClient....".

Download the simulation environment and install the required libraries (requirements.txt), if your API is not running on localhost port 5000 you may need to change that in APILink.py. 

Setup the config for the simulation you would like to perform (or leave blank for random generation), detailed instructions for how to construct the config.txt can be found in the accompaning "config-instructions.txt". Be warned that setting a high amount of sellers/bidders (especially with random chainlength) will cause the reference calculation to take quite a while.

After this is done you can start the program by running "main.py", it will first generate all the input data such as blocks, sellers and buyers. This will get computed by the reference calculation to get a fairness value and market price for the optimal match between blocks and buyers.

After this is done the simulator will start and the program will terminate after it has completed it's run. 

After a finished run several csv files will be saved in the file path of the project, which run the files belong to can be identified by the digit in the file name.

* test*.csv - Finished auction result, fairness value and buyer final status.
* testE*.csv - All the bids which were submitted by the buyers throughout the simulation, id stands for in which batch of bids they were sent.
* testJbidder*.csv - The configuration of the buyers which were used
* testJseller*.csv - The configuration of the sellers and blocks they have
* refcalcOutdata.csv (optional) - Details related to the reference calculation (needs to be manually enabled in ReferenceCalculator.py line 24)

## Sequence Diagram

<img src="images/sequence.png" width="75%" height="75%">

This diagram shows the rough process of the simulation.

## Class Diagram

<img src="images\classes.png" width="75%" height="75%">

## Behaviour library

There are 3 types of behaviours:

1. A: This is the most aggressive behaviour that will try to bid aggressively with higher bids and bid early.
2. B: This behaviour is a mixture of behaviour A and C that is medium aggressive.
3. C: This is the most passive behaviour and will most likely bid late with lower bids.

### Dictionary keys

Every behaviour has the dictionary keys:

1. "behaviour": This is what type of behaviour it is.
2. "agressiveness": A number between 0 and 1 that tells how aggressive the bidder is. It affects the bid amount and desperation.
3. "adaptiveAggressiveness": Updates the aggressiveness depending on the current round and the max round.
4. "desperation": It is a number between 0 and 1 and tells how likely it is for a bidder to bid depending on the aggressiveness, current round and the max round. 
5. "bidOverMarketPrice": This tells if the bidder can bid over the market price or not.
6. "marketPriceFactor": This affects the bid amount based on normal distribution with a mean and standard deviation value and the aggressiveness.
7. "marketPriceFactorUpdate": This updates the marketPriceFactor value depending on the aggressiveness, mean and standard deviation value.
8. "stopBid": This is the amount of bid that the bidder can't bid over and it's also the maximum bid on an auction. It's in price/unit.

## Reference Calculation
The reference calculation will look through almost every way the blocks of products can be distributed among the sellers to find the greatest Raj Jain fairness. This will result in many combinations being tested, the exact amount being printed before the function starts its calculations. The function will give periodic updates on its progress in order to help estimate the amount of time. 
If one wants a short running time one should:
1. Keep the number of blocks low.
2. Keep the number of buyers/bidders either very low or very close to the number of blocks. 
3. Not have Reference Calculation output enabled unless one is interested in the data.

### Reference Calculation Output
Near the end of the code in main.py inside the callOnReferenceCalculator function one can add True as a third argument to referenceCalculation in order to enable output of reference calculation data. Refcalc will then output a .csv-file containing all valid ways blocks of products can be bought by the buyers. It will also have data on the blocks bought, the average price paid, the calculated Raj Jain fairness and is ready to be built out to also accept distance and average distance as variables.

### Discounts
For the reference calculation discounts are a thing that is taken into account. These are automatically generated unless one manually defines the discounts according to the instructions in "config-instructions.txt". Discount is defined as the percentage unit difference in discount compares to the previous block of products. So if you for instance want blocks with a 0% | 4% | 7% | 9% | 10% discount they should be input as 0 | 4 | 3 | 2 | 1.

