names = {
	"trump": "realDonaldTrump",
	"clinton": "HillaryClinton",
	"sanders": "SenSanders"
}

import tweepy
import re
import json
from random import shuffle

fp = open("../private/twitter_credentials.json", "r")
credentials = json.load(fp)
fp.close()

consumer_key = credentials["consumer_key"]
consumer_secret = credentials["consumer_secret"]
access_key = credentials["access_token_key"]
access_secret = credentials["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def save_tweet(tweet, fp):
	tweet = tweet.text.encode("ascii", errors="ignore").decode()
	tweet = re.sub(r"[^ !\"#$%&'()*+,\-\./0-9:;=?@A-Z\[\]_a-z|~]", " ", tweet)
	tweet = re.sub(r"^[ ]+", "", tweet)
	tweet = re.sub(r"[ ]+$", "", tweet)
	tweet = re.sub(r"[ ]+", " ", tweet)
	tweet = tweet.replace("&amp;", "&")
	fp.write(tweet + "\n")

def get_all_tweets(screen_name, files_name):
	print("Getting tweets for: @" + screen_name)

	alltweets = []	
	new_tweets = api.user_timeline(screen_name=screen_name, count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1
	
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1
		print(len(alltweets), "tweets downloaded so far.")

	shuffle(alltweets)

	fp = open(files_name + "_test.txt", "w")
	for i in range(500):
		save_tweet(alltweets[i], fp)
	fp.close()
	fp = open(files_name + "_train.txt", "w")
	for i in range(500, len(alltweets)):
		save_tweet(alltweets[i], fp)
	fp.close()

for name in names:
	get_all_tweets(names[name], "../data/" + name)
