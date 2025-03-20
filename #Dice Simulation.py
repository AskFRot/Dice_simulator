#Dice Simulation
#Note: This script simulates and calculates the probabilities of reaching a target number when rolling two 20-sided dice, with the following conditions:
#Advantage (i.e. two dice and as long as one is greater than or equal to the target it succeeds).
#Disadvantage (i.e. two dice and as long as one is less than the target it fails).
#This script also compares these probabilities with a standard roll.
import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##Calculation
###Now this is what I did last (probably should have started with this), and it is just for calculating the probability, no simulating it.
###Figured having it first would allow you to check whether the rest is accurate.
def probability(dice_size, number, adv):
    if adv == True:
        return(((dice_size**2)-(number-1)**2)/dice_size**2)
    if adv == False:
        return(((dice_size-(number-1))**2)/dice_size**2)
    
advantages = []
disadvantages = []

for x in range(20, 0, -1):
    disadvantages.append(probability(20, x, False))
    advantages.append(probability(20, x, True))

num_rows=20
table=np.zeros((num_rows, 4))
table[:,0]=np.arange(num_rows, 0, -1)
table[:,1]=np.arange(0.05, 1.05, 0.05)
table[:,2]=advantages
table[:,3]=disadvantages

print(f"{'Target':<10} {'Normal':<10} {'Advantage':<10} {'Disadvantage':<10}")
for row in table:
    print(f"{int(row[0]):<10} {row[1]:<10.4f} {row[2]:<10.4f} {row[3]:<10.4f}")


##First approach using while True loop and simultanious advantage/disadvantage
advantage=[]
disadvantage=[]
simulations=10000
while True:
    #Do two dice rolls
    x = random.randrange(1, 21)
    y = random.randrange(1, 21)
    #Put the lower result into the disadvantage bin and the highest into the advantage bin
    if x >= y:
        advantage.append(x)
        disadvantage.append(y)
    if y > x:
        advantage.append(y)
        disadvantage.append(x)
    #When there are n results in the advantage bin, break the loop.
    if len(advantage)>=simulations:
        print(f"{len(advantage)}'s simulations done")
        break

###Sort and cumulative probability of advantage + disadvantage
###The sorting part is neccessary when doing it this way as I'm using the index of the first unique results to figure out the position, and adding that with the count allows us to count all the 20's, then all the 20's and 19's etc.
sorted_advantage = sorted(advantage, reverse=True)
sorted_disadvantage = sorted(disadvantage, reverse=True)
advantage_count_data = Counter(sorted_advantage)
disadvantage_count_data = Counter(sorted_disadvantage)
target = []
cdf_adv_value = []
cdf_disadv_value = []

###Create df with cumulative distribution function
for value in advantage_count_data:
    first_index = sorted_advantage.index(value)
    count = advantage_count_data[value]
    cdf_adv_value.append((first_index + count) / 10000)
    target.append(value)

for value in disadvantage_count_data:
    first_index = sorted_disadvantage.index(value)
    count = disadvantage_count_data[value]
    cdf_disadv_value.append((first_index + count) / 10000)

df = pd.DataFrame({
    'Target': target,
    'Advantage_CDF': cdf_adv_value,
    'Disadvantage_CDF': cdf_disadv_value
})
print(df)

###create a plot over the probability of reaching the target with advantage, disadvantage and normal respectivly
normal_line=-5*df['Target']+105

plt.figure(figsize=(10, 6))
plt.plot(df['Target'], df['Advantage_CDF'] * 100, label='Advantage', marker='o', color='blue')
plt.plot(df['Target'], df['Disadvantage_CDF'] * 100, label='Disadvantage', marker='o', color='red')
plt.plot(df['Target'], normal_line, label='Normal', marker='o', color='green' )

plt.xlabel('Target Number')
plt.ylabel('Percentage (%)')
plt.title('Advantage and Disadvantage Percentages')
plt.legend()
plt.grid(True)
plt.show()


##Last simulation try
###Now I wanted to take another shot at the simulation. Creating the bins for disadvantage and advantage at the same time was neat, but I'd rather not have it run in a while true loop, so I wanted to rewrite it all.
###Furthermore, the previous method was a struggle to get properly working at first, and I was iterating through the results quite unefficient at first before I cleaned it up a bit. However, it isnt as flexible as I'd like. Where I to add another variable, like more dice, I'd have rewrite the entierty, and it only does d20s.

#Creating the lists for the results. 
#Now we could have just made an empty list and appended the results. But we are rather iterating through and replacing the 0's in the lists with the function call.
simulations=10000
advantage = np.zeros(simulations)
disadvantage = np.zeros(simulations)

#Defining the dice roll functions.
def normal_roll():
    return(random.randrange(1,21))
def advantage_roll():
    return(max(normal_roll(), normal_roll()))
def disadvantage_roll():
    return(min(normal_roll(), normal_roll()))

#Iterating through the advantage/disadvantage list and replacing 0's with the dice rolls.
for n in range(simulations):
    advantage[n]=advantage_roll()
    disadvantage[n]=disadvantage_roll()

#Create emtpy variables for the cumulative probability
cumulative_disadv=0
cumulative_norm=0
cumulative_adv=0

cdf_data=[]

for i in range(20,0,-1):
    cumulative_disadv += np.sum(disadvantage==i) / simulations
    cumulative_norm += 0.05
    cumulative_adv += np.sum(advantage ==i) /simulations
    cdf_data.append({
        'Target': i,
        'Cumulative_Disadvantage': cumulative_disadv,
        'Cumulative_Advantage': cumulative_adv,
        'Cumulative_Normal': cumulative_norm
    })
    #This could be used to print out the distribution table.
    print(f"{i:2d} {cumulative_disadv:6.4f} {cumulative_norm:6.4f} {cumulative_adv:6.4f}")
#alternativly this can be used.
df = pd.DataFrame(cdf_data)

##Again, same plots as earlier
normal_line=-5*df['Target']+105

plt.figure(figsize=(10, 6))
plt.plot(df['Target'], df['Cumulative_Advantage'] * 100, label='Advantage', marker='o', color='blue')
plt.plot(df['Target'], df['Cumulative_Disadvantage'] * 100, label='Disadvantage', marker='o', color='red')
plt.plot(df['Target'], normal_line, label='Normal', marker='o', color='green' )

plt.xlabel('Target Number')
plt.ylabel('Percentage (%)')
plt.title('Advantage and Disadvantage Percentages')
plt.legend()
plt.grid(True)
plt.show()