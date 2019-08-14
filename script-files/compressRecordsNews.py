import datetime
from os import listdir
import csv
from os.path import isfile, join
files = [f for f in listdir("NewsPredictions") if isfile(join("NewsPredictions", f))]
for file in files:
	dateToPrice = dict()
	dateToPriceUpdated = dict()
	with open("NewsPredictionsUpdated/"+file,"w+") as predFile:
		fw=csv.writer(predFile, dialect='excel')
		with open("NewsPredictions/"+file,encoding='latin') as newFile:
			for i in newFile.readlines()[1:]:
				no,date,predicted,actual = i.strip().split(",")
				if date not in dateToPrice:
					dateToPrice[date] = []
				dateToPrice[date].append(float(predicted))
			
			for date in dateToPrice:
				avgStockPrice = sum(dateToPrice[date])/len(dateToPrice[date])
				if date >= '2017-11-16':

					year,mon,day = date.strip().split("-")
					nDate=datetime.date(int(year),int(mon),int(day)) - datetime.timedelta(days=31)
					day = str(nDate).split("-")[2]
					mon = str(nDate).split("-")[1]
					if day == "31" and int(mon)%2 == 1:
						continue
					mon = int(mon) + 5
					mon = (mon%12)

					year = int(year) + 1
					predDate = str(year)+"-"+str(mon)+"-"+str(day)
					nDate = datetime.date(int(year),int(mon),int(day))
					day = str(nDate).split("-")[2]
					mon = str(nDate).split("-")[1]
					year = str(nDate).split("-")[0]
					predDate = str(year)+"-"+str(mon)+"-"+str(day)
					l = [predDate,avgStockPrice]
					fw.writerow(l)
				



				
