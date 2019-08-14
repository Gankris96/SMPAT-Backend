import codecs, json
import re
import csv
import datetime

symbol = "ZYDUSWELL"
stockList = []
stockDict = {}
with open("companyStocksUpdated/"+symbol+".csv") as stockFile:
    for i in stockFile.readlines():
        stock = i.strip().split(",")
        stockList.append(stock)
for i in range(len(stockList)):
    stockDict[stockList[i][0]] = []
    for j in range(min(5,len(stockList)-i)):
        stockDict[stockList[i][0]].append(stockList[i+j][1])

count = 0
correctCount = 0
with open("TwitterCompanyNewsStock/"+symbol+".csv","w+") as newFile:
	fw=csv.writer(newFile, dialect='excel')
	with codecs.open('tweets/zydusWell.json','r','utf-8') as f:
		tweet = json.load(f,encoding='utf-8')
		for t in tweet:
			try:
				text = t['text'].split('http')[0]
				text = re.sub(r'\n+',' ',text)
				text = text.replace(","," ")
				
				if 'retweet' in text or text == '':
					continue
				time = t['timestamp'].split('T')[0]

				date1 = datetime.datetime.strptime(time,"%Y-%m-%d")
				date1s = date1.strftime('%Y-%m-%d')
				date2 = date1 + datetime.timedelta(days=1)
				date2s = date2.strftime('%Y-%m-%d')
				date3 = date2 + datetime.timedelta(days=1)
				date3s = date3.strftime('%Y-%m-%d')
				date4 = date3 + datetime.timedelta(days=1)
				date4s = date4.strftime('%Y-%m-%d')
				date5 = date4 + datetime.timedelta(days=1)
				date5s = date5.strftime('%Y-%m-%d')
				
				if date1s in stockDict:
					l = [t['timestamp'],text,stockDict[date1s][0],stockDict[date1s]]
				elif date2s in stockDict:
					l = [t['timestamp'],text,stockDict[date2s][0],stockDict[date2s]]
				elif date3s in stockDict:
					l = [t['timestamp'],text,stockDict[date3s][0],stockDict[date3s]]
				elif date4s in stockDict:
					l = [t['timestamp'],text,stockDict[date4s][0],stockDict[date4s]]
				elif date5s in stockDict:
					l = [t['timestamp'],text,stockDict[date5s][0],stockDict[date5s]]
				else:
					print("No date")
				correctCount += 1
				
				fw.writerow(l)
				
			except:
				count += 1
				#print("Stock price doesn't exist for the day")

# print(stockDict['2013-07-29'])
print(count)
print(correctCount)
