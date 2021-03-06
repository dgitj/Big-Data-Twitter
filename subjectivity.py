# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib import ticker
from collections import Counter
import numpy as np
import operator


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


###############################################
#Sentiment analysis
###############################################

my_tweets.rewind() 
from textblob import TextBlob
import re
positive = 0
negative = 0
neutral = 0



def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
clean_tweet



subjectivity = []
def tweet_sentiment_sub(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    return tweet_analysis.subjectivity

def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    
    if tweet_analysis.subjectivity > 0:
        return 'positive'

    elif tweet_analysis.subjectivity == 0:
        return 'neutral'

    else:
        return 'negative'

for tweet in my_tweets:
        
        subjectivity.append(tweet_sentiment_sub(tweet['text']))
        
        if tweet_sentiment(tweet['text']) == 'positive':
                positive = positive+1;
                

        if tweet_sentiment(tweet['text']) == 'neutral':
                neutral = neutral+1;
                

        if tweet_sentiment(tweet['text']) == 'negative':
                negative = negative+1;



num_bins = 50
plt.figure(figsize=(10,6))
n, bins, patches = plt.hist(subjectivity, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Subjectivity')
plt.ylabel('Count')
plt.title('Histogram of subjectivity')
plt.show()

        
