from os import listdir
import csv
from os.path import isfile, join
import datetime
files = [f for f in listdir("Pred_Twitter") if isfile(join("Pred_Twitter", f))]
for file in files:
	dateToPrice = dict()
	dateToPriceUpdated = dict()
	with open("twitterPredictionUpdated/"+file,"w+") as predFile:
		fw=csv.writer(predFile, dialect='excel')
		with open("Pred_Twitter/"+file,encoding='latin') as newFile:
			for i in newFile.readlines()[1:]:
				no,date,predicted,actual = i.strip().split(",")
				if date not in dateToPrice:
					dateToPrice[date] = [float(actual)]
				dateToPrice[date].append(float(predicted))
			for date in dateToPrice:
				if(date >= '2018-02-01'):
					avgStockPrice = sum(dateToPrice[date][1:])/len(dateToPrice[date][1:])
					year,month,day = date.strip().split("-")
					nDate=datetime.date(int(year),int(month),int(day)) - datetime.timedelta(days=15)
					day = str(nDate).split("-")[2]
					mon = str(nDate).split("-")[1]
					if day == "31" and int(mon)%2 == 1:
						continue
					
					nDate = nDate + datetime.timedelta(days=30)
					day = str(nDate).split("-")[2]
					mon = str(nDate).split("-")[1]
					year = str(nDate).split("-")[0]
					predDate = str(year)+"-"+str(mon)+"-"+str(day)
					l = [predDate,avgStockPrice,dateToPrice[date][0]]
					fw.writerow(l)
