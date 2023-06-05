import tweepy
import sys
import os
import mysql.connector
from dotenv import load_dotenv

# print("halo dunia")

load_dotenv()
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_secret = os.getenv("access_secret")

tweetsPerQry = 5
maxTweets = 10
for arg in sys.argv:
    # print(arg)
    pass
hashtag = sys.argv[1]
# print(hashtag)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="deteksi_trending_topik"
)

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)
maxId = -1
tweetCount = 0
mycursor = mydb.cursor()
newTweets = tweepy.Cursor(api.search_tweets, q=hashtag,
                          tweet_mode="extended").items(maxTweets)

newTweets = [x for x in newTweets]

total = 0
val = []
for tweet in newTweets:
    if 'retweeted_status' in dir(tweet):
        text = tweet.retweeted_status.full_text
    else:
        text = tweet.full_text
    user_screen_name = tweet.user.screen_name
    tweet_tuple = (
        user_screen_name,
        text
    )
    query = "SELECT * FROM dokumen WHERE text=%s"
    mycursor.execute(query, (text,))

    x = [i for i in mycursor]

    if x == []:
        val.append(tweet_tuple)

sql = '''
    INSERT INTO dokumen (user_screen_name, text) 
    VALUES (%s,%s)
'''
mycursor.executemany(sql, val)

mydb.commit()
tweetCount += len(newTweets)
maxId = newTweets[-1].id
