# Python3 program to find maximum
# achievable value with a knapsack
# of weight W and multiple instances allowed.
 
# Returns the maximum value 
# with knapsack of W capacity

import csv

def instancesUsed(items,weights, capacity,size,companyList,dateList):
	k = capacity
	instances = []
	for i in range(size):
		instances.append(0)
	while(k >= 0):
		x = items[k]
		if(x == -1):
			break
		instances[x] += 1
		k -= weights[items[k]]
	recommend = ""
	for i in range(size):
		if instances[i] != 0:
			# print(weights[i],"--->",instances[i])
			# print(companyList[i],"--->",dateList[i])
			recommend += "Invest "+str(instances[i])+" stocks on "+str(companyList[i])+" on "+str(dateList[i])+" for Rs."+str(weights[i])+" per stock\n"
	return recommend
def unboundedKnapsack(weights,values,items,n,capacity,companyList,dateList):
	knapsack = [0 for i in range(capacity+1)]
	knapsack[0] = 0
	items[0] = -1
	for j in range(1,capacity+1):
		items[j] = items[j-1]
		maxK = knapsack[j-1]
		for i in range(n):
			x = j - weights[i]
			if(x >= 0 and (knapsack[x]+values[i]) > maxK):
				maxK = knapsack[x] + values[i]
				items[j] = i
		knapsack[j] = maxK
	return knapsack[capacity]
 
capacity = 5000 #Amount
values = []
weights = []
companyList = []
dateList = []
with open("Recommender.csv") as file:
	for record in file.readlines():
		company,date,gain,closingPrice = record.strip().split(",")
		values.append(int(round(float(gain))))
		weights.append(int(round(float(closingPrice))))
		companyList.append(company)
		dateList.append(date)

# Driver program

# values = [800,900, 900,800] #Gains incurred
# weights = [2700,2100,900,800] #Closing prices of the company
size = len(values)
items = [0 for i in range(capacity+1)]
print()
recommend = "Total Gain received: Rs"+str(unboundedKnapsack(weights,values,items,size,capacity,companyList,dateList))+"\n"
recommend += instancesUsed(items,weights,capacity,size,companyList,dateList)

with open("RecommendedStocks.txt","w+") as f:
	f.write(recommend)

