import tweepy
import time, datetime
from pymongo import MongoClient

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
			tempDate = tweet._json['created_at']
			unixTime = time.mktime(datetime.datetime.strptime(tempDate, "%a %b %d %H:%M:%S +0000 %Y").timetuple())
			tweet._json['created_at'] = unixTime
			tweet._json['showableDate'] = datetime.datetime.fromtimestamp(unixTime).strftime('A las %I:%M %p del %A %d de %B del %Y')
			tweetCollection.insert_one(tweet._json)
			insertedCount = insertedCount + 1
			# print("####################################################################################NEW TWEET")
			# pp.pprint(tweet._json)
		#If it is then ignore it
		
retrieveTweets()

	# print("New tweets inserted: "+str(insertedCount))