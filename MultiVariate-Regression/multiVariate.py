import csv
from os import listdir
from os.path import isfile, join
import datetime
from math import ceil
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
monthMap = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
def multiVariate(symbol): 
	consolidatedRnn = dict()
	with open("RRNPredictionsUpdated/Predictions_"+symbol+".csv") as rnnFile:
		for rnnPred in rnnFile.readlines():
			StockDate,predictedPrice,actualPrice = rnnPred.strip().split(",")
			if StockDate not in consolidatedRnn:
				consolidatedRnn[StockDate] = [StockDate]
				consolidatedRnn[StockDate].append(float(actualPrice))
				

			consolidatedRnn[StockDate].append(float(predictedPrice))
	consolidatedNews = dict()
	try:
		with open("NewsPredictionsUpdated/Predict_"+symbol+"_FINAL.csv") as newsFile:
			for newsPred in newsFile.readlines():
				StockDate, predictedPrice = newsPred.strip().split(",")
				if StockDate not in consolidatedNews:
					consolidatedNews[StockDate] = []
				consolidatedNews[StockDate].append(float(predictedPrice))	
		
		consolidatedTwit = dict()
		with open("twitterPredictionUpdated/"+symbol+"_Final.csv") as twitFile:
			for twitPred in twitFile.readlines():
				StockDate, predictedPrice, actualPrice = twitPred.strip().split(",")
				if StockDate not in consolidatedTwit:
					consolidatedTwit[StockDate] = []
				consolidatedTwit[StockDate].append(float(predictedPrice))
				consolidatedTwit[StockDate].append(float(actualPrice))
				consolidatedTwit[StockDate].append(StockDate)
	except:
		print("No news and tweet predictions")
		final = dict()
		for i in consolidatedRnn:
				final[i] = []
				final[i].extend(consolidatedRnn[i])
		

		data = []
		for i in final:
			data.append(final[i])
		
		predictedPriceFinalList = []
		actualPriceList = []
		DateList = []
		for instance in data:
			rnnPrice = instance[2]
			actualPrice = instance[1]

			PredictedPriceFinal = ((rnnPrice + actualPrice)/2.0)
			predictedPriceFinalList.append(PredictedPriceFinal)
			actualPriceList.append(actualPrice)
			DateList.append(instance[0])
		
		with open("finalRegression/"+symbol+".csv","w+") as f:
			writer = csv.writer(f)
			
			for i in range(len(predictedPriceFinalList)):
				l = [DateList[i], predictedPriceFinalList[i]]
				writer.writerow(l)
		predictedPriceNpList = []
		actualPriceNpList = []
		for i in range(len(predictedPriceFinalList)):
			predictedPriceNpList.append(np.array([predictedPriceFinalList[i]]))
			actualPriceNpList.append(np.array(actualPriceList[i]))
		predictedPriceNpList = np.array(predictedPriceNpList)
		actualPriceNpList = np.array(actualPriceNpList)
		# print(predictedPriceFinalList)
		print(predictedPriceNpList)
		plt.plot(predictedPriceNpList, color = 'red', label = 'Real' + symbol+' Stock price')
		plt.title(symbol+' Stock price prediction')
		plt.xlabel('Days')
		plt.ylabel(symbol+' Stock Price')
		plt.savefig("finalRegressionImages/"+symbol+".jpg")
		return
	final = dict()
	for i in consolidatedRnn:
		if i in consolidatedTwit and i in consolidatedNews:

			final[i] = []
			final[i].extend(consolidatedRnn[i])
			final[i].extend(consolidatedNews[i])
			final[i].extend(consolidatedTwit[i][:-1])
	

	data = []
	for i in final:
		data.append(final[i])
	
	predictedPriceFinalList = []
	actualPriceList = []
	DateList = []
	for instance in data:
		rnnPrice = instance[2]
		newsPrice = instance[3]
		tweetPrice = instance[4]
		actualPrice = instance[1]

		rnnDiff = abs(actualPrice - rnnPrice)
		newsDiff = abs(actualPrice - newsPrice)
		tweetDiff = abs(actualPrice - tweetPrice)
		weight = (1.0/rnnDiff)+(1.0/newsDiff)+(1.0/tweetDiff)

		rnnWeight = (1.0/rnnDiff)/weight
		tweetWeight = (1.0/tweetDiff)/weight
		newsWeight = (1.0/newsDiff)/weight

		PredictedPriceFinal = rnnWeight*rnnPrice + newsWeight*newsPrice + tweetWeight*tweetPrice
		predictedPriceFinalList.append(PredictedPriceFinal)
		actualPriceList.append(actualPrice)
		DateList.append(instance[0])
	
	with open("finalRegression/"+symbol+".csv","w+") as f:
		writer = csv.writer(f)
		
		for i in range(len(predictedPriceFinalList)):
			l = [DateList[i], predictedPriceFinalList[i]]
			writer.writerow(l)
	predictedPriceNpList = []
	actualPriceNpList = []
	for i in range(len(predictedPriceFinalList)):
		predictedPriceNpList.append(np.array([predictedPriceFinalList[i]]))
		actualPriceNpList.append(np.array(actualPriceList[i]))
	predictedPriceNpList = np.array(predictedPriceNpList)
	actualPriceNpList = np.array(actualPriceNpList)
	# print(predictedPriceFinalList)
	print(predictedPriceNpList)
	plt.plot(predictedPriceNpList, color = 'red', label = 'Real' + symbol+' Stock price')
	plt.title(symbol+' Stock price prediction')
	plt.xlabel('Days')
	plt.ylabel(symbol+' Stock Price')
	plt.savefig("finalRegressionImages/"+symbol+".jpg")
	# plt.show()

	"""
	data = np.array(data)
	x_dataTrain = data[:ceil(0.8*len(data)),1:]
	y_dataTrain = data[:ceil(0.8*len(data)),0]
	x_dataTest = data[ceil(0.8*len(data)):,1:]
	y_dataTest = data[ceil(0.8*len(data)):,0]
	ols = linear_model.LinearRegression()
	model = ols.fit(x_dataTrain,y_dataTrain)
	y_dataTestPred = model.predict(x_dataTest)
	y_dataTest = np.array(y_dataTest)
	dataToCsv = []
	rmse = 0
	sumSquares = 0
	for i in range(len(y_dataTest)):
		diff = y_dataTest[i] - y_dataTestPred[i]
		diffSquare = diff**2
		sumSquares += diffSquare
	rmse = (sumSquares/len(y_dataTest))**0.5

	for i in range(len(y_dataTest)):
		temp = [y_dataTest[i],y_dataTestPred[i],y_dataTest[i] - y_dataTestPred[i],rmse]
		dataToCsv.append(temp)
	with open("finalRegression.csv", "w+") as f:
		writer = csv.writer(f)
		writer.writerow(["Actual","Prediction","Difference","rmse"])
		writer.writerows(dataToCsv)
	"""

# symbols = ["INFY","ASHOKLEY","BAJAJ-AUTO","BIOCON","CASTROLIND","CENTURYPLY","CESC","COLPAL","COX-KINGS","DABUR","GREENPLY","HCLTECH","HEROMOTOCO","HOTELEELA","INDBANK","INFIBEAM","JSWENERGY","LAKSHVILAS","MAHSCOOTER","MARUTI","MEP","MHRIL","MINDTREE","NATCOPHARM","NIITTECH","NOCIL","PETRONET","RELIANCE"]
# for symbol in symbols:
# 	multiVariate(symbol)
multiVariate("ZYDUSWELL")
