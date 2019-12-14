#from __future__ import division
import shapely
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib import ticker
from collections import Counter
import numpy as np
import operator
import seaborn as sns
import pandas as pd
import descartes
import cartopy.crs as ccrs
from matplotlib.patches import Circle
from itertools import product
import statistics

from textblob import TextBlob
import re


#api key google, places: AIzaSyAjZWHtwxWWlHfJPODzbF8JAMaa5EVN9Kw


# Establish connection with database
client = MongoClient()
db = client.gt
col = db.twitterBrazil

#######################################################
# Retrieve data from the mongodb database, choosing
# the fields you'll need afterwards
#######################################################
my_tweets = db.twitterBrazil.find({},{'lang':1, '_id':0, 'id':1, 'text':1, 'entities.hashtags':1, 'geo':1, 'location':1, 'coordinates':1, 'place':1,
'in_reply_to_status_id':1, 'is_quote_status':1, 'retweeted_status':1, 'user.screen_name':1} )
numTweets = db.twitterBrazil.count()

# list with the 'place', 'bounding_box' and 'coordinates' values of the tweet
location = []
countries = []
cities = []
country_codes = []



# get the values for the location list
for i in my_tweets:
    if i['place'] != None:
        loc = i['place']
        location.append(loc)

for i in location:
    country = i['country']
    countries.append(country)

for i in location:
    city = i['name']
    cities.append(city)

for i in location:
    country_code = i['country_code']
    country_codes.append(country_code)


#group by
m = pd.DataFrame({'country': countries, 'city': cities, 'code': country_codes })
count = m.groupby(['code']).size().to_frame('count').reset_index()
ordered_count = count.sort_values(by=['count'])
count_list = ordered_count.astype({'count': int})

my_tweets.rewind()
#print(count_list[-20:])
#print(len(location))


my_tweets.rewind()
#US tweets
us_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "US":
             us_tweets.append(i['text'])

#CA tweets
my_tweets.rewind()
ca_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "CA":
             ca_tweets.append(i['text'])

#GB tweets
my_tweets.rewind()
gb_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "GB":
             gb_tweets.append(i['text'])


#BR tweets
my_tweets.rewind()
br_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "BR":
             br_tweets.append(i['text'])

#AU tweets
my_tweets.rewind()
au_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "AU":
             au_tweets.append(i['text'])


#IN tweets
my_tweets.rewind()
in_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "IN":
             in_tweets.append(i['text'])


#FR tweets
my_tweets.rewind()
fr_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "FR":
             fr_tweets.append(i['text'])


#ES tweets
my_tweets.rewind()
es_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "ES":
             es_tweets.append(i['text'])

#SE tweets
my_tweets.rewind()
se_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "SE":
             se_tweets.append(i['text'])

#DE tweets
my_tweets.rewind()
de_tweets = []
for i in my_tweets:
    if i["place"] is not None and i['place']['country_code']  == "DE":
             de_tweets.append(i['text'])




############################################
#sentiment
###########################################
sentiment = []

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
clean_tweet



def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    
    return tweet_analysis.polarity
    


us_sentiment = []
ca_sentiment = []
gb_sentiment = []
br_sentiment = []
au_sentiment = []
in_sentiment = []
fr_sentiment = []
es_sentiment = []
se_sentiment = []
de_sentiment = []

for t in us_tweets:
    us_sentiment.append(tweet_sentiment(t))

for t in ca_tweets:
    ca_sentiment.append(tweet_sentiment(t))

for t in gb_tweets:
    gb_sentiment.append(tweet_sentiment(t))

for t in br_tweets:
    br_sentiment.append(tweet_sentiment(t))

for t in au_tweets:
    au_sentiment.append(tweet_sentiment(t))

for t in in_tweets:
    in_sentiment.append(tweet_sentiment(t))

for t in fr_tweets:
    fr_sentiment.append(tweet_sentiment(t))

for t in es_tweets:
    es_sentiment.append(tweet_sentiment(t))

for t in se_tweets:
    se_sentiment.append(tweet_sentiment(t))

for t in de_tweets:
    de_sentiment.append(tweet_sentiment(t))

mean1 = statistics.median(us_sentiment)
mean2 = statistics.median(ca_sentiment)
mean3 = statistics.median(gb_sentiment)
mean4 = statistics.median(br_sentiment)
mean5 = statistics.median(au_sentiment)
mean6 = statistics.median(in_sentiment)
mean7 = statistics.median(fr_sentiment)
mean8 = statistics.median(es_sentiment)
mean9 = statistics.median(se_sentiment)
mean10 = statistics.median(de_sentiment)



print(mean1)
print(mean2)
print(mean3)   
print(mean4)
print(mean5)
print(mean6)
print(mean7)
print(mean8)
print(mean9)
print(mean10)