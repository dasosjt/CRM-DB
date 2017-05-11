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


def retrieveTweets():
	lastTweets = api.home_timeline(count=100)
	insertedCount = 0

	for tweet in lastTweets:
		#Check if tweet is already in the database
		if(tweetCollection.find_one({'id':tweet.id}) == None):
			#If it doesn't then insert it
			tweetCollection.insert_one(tweet._json)
			insertedCount = insertedCount + 1
			# print("####################################################################################NEW TWEET")
			# pp.pprint(tweet._json)
		#If it is then ignore it

	# print("New tweets inserted: "+str(insertedCount))


def followUsername(username):
	print("Function called!")
	api.create_friendship(screen_name=username)

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
	print(query)

	return tweetCollection.find(query)