# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib import ticker
from collections import Counter
import numpy as np
import operator
import csv
from textblob import TextBlob
import re

# Establish connection with database
client = MongoClient()
db = client.gt
col = db.twitterBrazil

#######################################################
# Retrieve data from the mongodb database, choosing
# the fields you'll need afterwards
#######################################################
my_tweets = db.twitterBrazil.find({},{'lang':1, '_id':0, 'text':1, 'entities.hashtags':1,
'in_reply_to_status_id':1, 'is_quote_status':1, 'retweeted_status':1, 'user.screen_name':1} )
numTweets = db.twitterBrazil.count()


##########################################
#only original content
########################################

original = []
for tweet in my_tweets:
    if tweet.get('retweet_status') is None and tweet.get('is_quote_status') is None and tweet.get('in_reply_to_status_id') is None:
        original.append(tweet['text'])

print(len(original))
###############################################
#Sentiment analysis
###############################################

my_tweets.rewind() 


positive = 0
negative = 0
neutral = 0



def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
clean_tweet



polarity = []
def tweet_sentiment_pol(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    return tweet_analysis.polarity

def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    
    if tweet_analysis.polarity > 0:
        return 'positive'

    elif tweet_analysis.polarity == 0:
        return 'neutral'

    else:
        return 'negative'

tweet_text = []
for tweet in my_tweets:
        
        polarity.append(tweet_sentiment(tweet['text']))
        tweet_text.append(tweet['text'])
        
        
        if tweet_sentiment(tweet['text']) == 'positive':
                positive = positive+1
                

        if tweet_sentiment(tweet['text']) == 'neutral':
                neutral = neutral+1
                

        if tweet_sentiment(tweet['text']) == 'negative':
                negative = negative+1


# print(*polarity[:10], sep='\n')
# print(*tweet_text[:10], sep = '\n')

######################################
#Export tweet +  sentiment to csv for better readability
######################################

