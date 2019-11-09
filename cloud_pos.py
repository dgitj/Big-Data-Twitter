# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import operator
from statistics import mode
from textblob import TextBlob
import re

from twython import Twython
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from IPython.display import Image as im


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


positive = 0
negative = 0
neutral = 0


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
clean_tweet




hashList = []

pos_tweets = []


def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    
    if tweet_analysis.polarity > 0:
        return 'positive'

    elif tweet_analysis.polarity == 0:
        return 'neutral'

    else:
        return 'negative'
    
my_tweets.rewind()

for t in my_tweets:
    if tweet_sentiment(t['text']) == "positive":
               pos_tweets.append(t)



my_tweets.rewind()

tweets = []

for e in pos_tweets:
    tweets.append(e['text'])


#Create a string form of our list of text
tweets = ''.join(tweets)
no_links = re.sub(r'hxttp\S+', '', tweets)
no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
no_special_characters = re.sub('[^A-Za-z ]+', '', no_unicode)

words = no_special_characters.split(" ")
words = [w for w in words if len(w) > 2]  # ignore a, an, be, ...
words = [w.lower() for w in words]
words = [w for w in words if w not in STOPWORDS]

def most_common(words): 
    return(mode(words)) 

print(most_common(words))


mask = np.array(Image.open('baum.png'))

wc = WordCloud(background_color="white", max_words=2000, mask=mask)
clean_string = ','.join(words)
wc.generate(clean_string)


f = plt.figure(figsize=(50,50))
f.add_subplot(1,2, 1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.title('Original Stencil', size=40)
plt.axis("off")
f.add_subplot(1,2, 2)
plt.imshow(wc, interpolation='bilinear')
plt.title('Twitter Generated Cloud', size=40)
plt.axis("off")
plt.show()
         