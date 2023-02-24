import random

numseller=random.randrange(5,20)
supply=[]
sumseller=0
for x in range(numseller):
    rng = random.randrange(100,1000)
    sumseller = sumseller + rng
    supply.append(rng)


numbuyers=random.randrange(5,15)
demand=[]
sum=0
for x in range(numbuyers):
    rng = random.randrange(100,1000)
    sum = sum + rng
    demand.append(rng)



print("demand sum",sum)
print(demand)
print("supply sum", sumseller)
print(supply)

sumnew=0
for x in demand:
    x=x/sum
    x=x*sumseller
    sumnew = sumnew + x
    print(x)
print(sumnew)