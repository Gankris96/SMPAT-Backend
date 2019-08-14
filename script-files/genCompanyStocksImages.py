import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
import csv
from os.path import isfile, join
def genImages(symbol):
	print(symbol)
	real_stock_price_train = pd.read_csv('companyStockValidation/'+symbol+'.csv')
	real_stock_price_train = real_stock_price_train.iloc[-90:,3:].values



	# Visualising the results
	plt.plot(real_stock_price_train, color = 'red', label = 'Real '+symbol+' Stock Price')
	plt.xlabel('Days')
	plt.ylabel(symbol+' Stock Price')
	plt.legend()
	plt.savefig("companyStocksImages/"+symbol+".jpg")



genImages("TECHM")
