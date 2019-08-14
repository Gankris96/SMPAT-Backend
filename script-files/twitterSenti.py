from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import preprocessor as p #cleaning each tweet using tweet-preprocessor like removing hashtags,urls,emojis....
import re
import csv
from os import listdir
from os.path import isfile, join
files = [f for f in listdir("TwitterCompanyNewsStock") if isfile(join("TwitterCompanyNewsStock", f))]
def function_udf(input_str):
    input_str = re.sub(r'RT', '', input_str)
    p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION)
    input_str = p.clean(input_str)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", input_str).split())

analyser = SentimentIntensityAnalyzer()
def senti_score_udf(sentence):
    snt = analyser.polarity_scores(sentence)
    return ([snt['neg'], snt['neu'], snt['pos'], snt['compound']])


for symbol in files:
	count = 0
	dateDict = {}
	dateFeatureDict = {}
	dateFeaturesDict = {}
	with open("TwitterCompanyNewsStock/"+symbol) as stockFile:
		for i in stockFile.readlines():
			try:
				i = i.split(",",3)
				date, tweet, closingPrice, closingPriceList = i[0].split("T")[0],i[1],i[2],i[3]
				# print("date:",date)
				# print("tweet:",tweet)
				# print("closingPrice:",closingPrice)
				# print("closingPriceList:",closingPriceList)
				cleanedTweet = function_udf(tweet)
				TweetNeg, TweetNeu, TweetPos, TweetComp = senti_score_udf(cleanedTweet)
				line = [i[0], cleanedTweet, closingPriceList, TweetNeg, TweetNeu, TweetPos, TweetComp, closingPrice]

				if date not in dateDict:
					dateDict[date] = []
				dateDict[date].append(line)
				if TweetComp > 0.4 or TweetComp < -0.4:
					featureLine = [i[0],TweetComp,closingPrice]
					featuresLine = [i[0],TweetNeg,TweetNeu,TweetPos,TweetComp,closingPrice]
					if date not in dateFeatureDict:
						dateFeatureDict[date] = []
						dateFeaturesDict[date] = []
					dateFeatureDict[date].append(featureLine)
					dateFeaturesDict[date].append(featuresLine)
			except:
				# print(i)
				count = count+1

	dateDictSorted = sorted(dateDict)
	dateFeatureDictSorted = sorted(dateFeatureDict)
	dateFeaturesDictSorted = sorted(dateFeaturesDict)
	with open("TwitterAllFeaturesSenti/"+symbol,"w+") as featuresFile:
		featuresAll = csv.writer(featuresFile, dialect='excel')
		with open("TwitterFeaturesSenti/"+symbol,"w+") as featureFile:
			featureHandler = csv.writer(featureFile, dialect='excel')
			with open("TwitterCompanyStockSenti/"+symbol,"w+") as sentiFile:
				fw=csv.writer(sentiFile, dialect='excel')
				for key in dateDictSorted:
					temp = dateDict[key]
					for j in temp:
						fw.writerow(j)
				for i in dateFeatureDictSorted:
					temp1 = dateFeatureDict[i]
					for j in temp1:
						if '"' in str(j[0]) or '"' in str(j[1]) or '"' in str(j[2]):
							continue
						featureHandler.writerow(j)

				for i in dateFeaturesDictSorted:
					temp1 = dateFeaturesDict[i]
					for j in temp1:
						if "[" not in j[5] and "\\" not in j[5]:
							featuresAll.writerow(j)
	print(count)