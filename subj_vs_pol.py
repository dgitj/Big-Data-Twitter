# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib import ticker
from collections import Counter
import numpy as np
import operator
import seaborn as sns
import pandas as pd


# Establish connection with database
client = MongoClient()
db = client.gt
col = db.twitterBrazil

#######################################################
# Retrieve data from the mongodb database, choosing
# the fields you'll need afterwards
#######################################################
my_tweets = db.twitterBrazil.find({},{'lang':1, '_id':0, 'id':1, 'text':1, 'entities.hashtags':1,
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
ids = []
def tweet_sentiment_sub(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    return tweet_analysis.subjectivity

for tweet in my_tweets: 
        subjectivity.append(tweet_sentiment_sub(tweet['text']))
        ids.append(tweet['id'])
        

##########################################
#polarity
#########################################

my_tweets.rewind() 
polarity = []


def tweet_sentiment_pol(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    return tweet_analysis.polarity

for tweet in my_tweets: 
        polarity.append(tweet_sentiment_pol(tweet['text']))
        


dataframe = pd.DataFrame(index = ids, data = {"subjectivity": subjectivity, "polarity": polarity}) 



#scatter for dffilter

sns.lmplot(x='subjectivity',y='polarity', data = dataframe,fit_reg=True,scatter=True, height=10,palette="mute") 
plt.show()
