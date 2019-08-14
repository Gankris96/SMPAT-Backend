import datetime
from os import listdir
import csv
from os.path import isfile, join
month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
files = [f for f in listdir("RNNPredictions") if isfile(join("RNNPredictions", f))]
averageRmse = 0
fileCount = 0
companies = []
for file in files:
	dateToPrice = dict()
	dateToActualPrice = dict()
	dateToPriceUpdated = dict()
	with open("RRNPredictionsUpdated/"+file,"w+") as predFile:
		fw=csv.writer(predFile, dialect='excel')
		with open("RNNPredictions/"+file,encoding='latin') as newFile:
			
			for i in newFile.readlines()[1:]:
				no,date,actual,predicted,df,sqdf,mdf,rmse = i.strip().split(",")
				if date not in dateToPrice:
					dateToPrice[date] = []
					dateToActualPrice[date] = []
					dateToActualPrice[date].append(actual)
				dateToPrice[date].append(float(predicted))
			count = 0
			sumDiffSqStockPrice = 0
			for date in dateToPrice:
				avgStockPrice = sum(dateToPrice[date])/len(dateToPrice[date])
				sumDiffSqStockPrice += (avgStockPrice - float(dateToActualPrice[date][0]))**2
				count += 1
				day,mon,year = date.strip().split("-")
				monthD = month[mon]
				newDate = day+"-"+monthD+"-"+year
				nDate=datetime.date(int(year),int(monthD),int(day))
				limitDate=datetime.date(2018,3,16)
				
				# input()
				if(nDate >= limitDate):
					# print(newDate,"Greater THAN",'16-03-2018')
					if day == "31" and int(monthD)%2 == 1:
						continue
					
					monthD = int(monthD) + 1
					
					predDate = year+"-"+str(monthD)+"-"+day
					nDate = datetime.date(int(year),int(monthD),int(day))
					day = str(nDate).split("-")[2]
					mon = str(nDate).split("-")[1]
					year = str(nDate).split("-")[0]
					predDate = str(year)+"-"+str(mon)+"-"+str(day)
					l = [predDate,avgStockPrice,str(float(dateToActualPrice[date][0]))]
					fw.writerow(l)

			if ((sumDiffSqStockPrice/count)**0.5 <= 5):
				fileCount += 1
				averageRmse += (sumDiffSqStockPrice/count)**0.5
				print(file,"----->",((sumDiffSqStockPrice/count)**0.5))
				companies.append(file)
print((averageRmse/fileCount))
print(fileCount)
print(companies)

