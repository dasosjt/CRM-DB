import tweepy
from pymongo import MongoClient
import time, datetime

#Pretty print for dictionaries (Debugging)
# import pprint
# pp = pprint.PrettyPrinter(indent=4)


#Mongo client setup
client = MongoClient('localhost', 27017)
db = client['CRM']
tweetCollection = db.tweets


#Twitter keys (From CRM account)
auth = tweepy.OAuthHandler('gdGthOGUNXmafP3vwv0bVIqH8', 'f7XjLfGxwli19CTGvjq73fEDiOEdIU8iDRsW0y4thxeTKHjK9N')
auth.set_access_token('861773027394113537-yqc3Q2IENArtKmnGmW1MjMX9AgV9CE3', 'T8ZWuBuMbkSYRriI3wToxWJK32DdHjBMKdA2yciQawUhz')


#Generate API object
api = tweepy.API(auth)


def followUsername(username):
	print("Function called!")
	#Follow the user for future tweet pulling
	api.create_friendship(screen_name=username)

def unfollowUsername(username):
	api.destroy_friendship(screen_name=username)


def getTweets(username, **filter_parameters):
	query = {'user.screen_name':username}
	for param in filter_parameters:
		if param == 'afterDate':
			if filter_parameters[param] != '':
				print("Trying to convert date: "+filter_parameters[param])
				tempDate = time.mktime(datetime.datetime.strptime(str(filter_parameters[param]), "%Y-%m-%d").timetuple())
				query['created_at'] = {"$gt":tempDate}
		elif param == 'beforeDate':
			if filter_parameters[param] != '':
				print("Trying to convert date: "+filter_parameters[param])
				tempDate = time.mktime(datetime.datetime.strptime(str(filter_parameters[param]), "%Y-%m-%d").timetuple())
				query['created_at'] = {"$lt":tempDate}
		elif param == 'containingWord':
			query['text'] = {"$regex":filter_parameters[param]}

	return tweetCollection.find(query)

def getStats(username):
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	dayStats = []
	for day in days:
		tempResult = tweetCollection.find({'user.screen_name':username, 'dayDate':day}).count()
		dayStats.append({'dayName':day, 'dayResult':tempResult})

	hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
	hourStats = []
	for hour in hours:
		tempResult = tweetCollection.find({'user.screen_name':username, 'hourDate':hour}).count()
		hourStats.append({'dayName':hour, 'hourResult':tempResult})

	return dayStats, hourStats
