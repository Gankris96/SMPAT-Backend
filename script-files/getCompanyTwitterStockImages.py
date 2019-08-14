import matplotlib.pyplot as plt
import pandas as pd

def genImages(symbol):

	real_stock_price_train = pd.read_csv('twitterPredictionUpdated/'+symbol+'_Final.csv')
	real_stock_price_train1 = real_stock_price_train.iloc[-30:,1:2].values
	real_stock_price_train2 = real_stock_price_train.iloc[-30:,2:].values



	# Visualising the results
	plt.plot(real_stock_price_train1, color = 'red', label = 'Predicted '+symbol+' Stock Price')
	plt.plot(real_stock_price_train2, color = 'blue', label = 'Real '+symbol+' Stock Price')
	plt.xlabel('Recent Tweets')
	plt.ylabel(symbol+' Stock Price')
	plt.legend()
	plt.savefig("companyTwitterStocksImages/"+symbol+".jpg")

genImages("BAJAJ-AUTO")