import matplotlib.pyplot as plt
import pandas as pd

def genImages(symbol):

	real_stock_price_train = pd.read_csv('NewsPredictions/Predict_'+symbol+'_FINAL.csv')
	real_stock_price_train1 = real_stock_price_train.iloc[-90:,2:3].values
	real_stock_price_train2 = real_stock_price_train.iloc[-90:,3:4].values
	


	# Visualising the results
	plt.plot(real_stock_price_train1, color = 'red', label = 'Real '+symbol+' Stock Price')
	plt.plot(real_stock_price_train2, color = 'blue', label = 'Predicted '+symbol+' Stock Price')
	plt.xlabel('Recent News Headlines')
	plt.ylabel(symbol+' Stock Price')
	plt.legend()
	plt.savefig("companyNewsStocksImages/"+symbol+".jpg")

genImages("SIEMENS")