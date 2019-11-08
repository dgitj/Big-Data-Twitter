# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
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

for tweet in my_tweets:
        
        polarity.append(tweet_sentiment_pol(tweet['text']))
        
        
        if tweet_sentiment(tweet['text']) == 'positive':
                positive = positive+1;
                

        if tweet_sentiment(tweet['text']) == 'neutral':
                neutral = neutral+1;
                

        if tweet_sentiment(tweet['text']) == 'negative':
                negative = negative+1;


################################################
#print sentiment histogram
###############################################

mu = 0  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=1)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(bins, y, '--')
ax.set_xlabel('tweets')
ax.set_ylabel(' density')
ax.set_title("sentiment")

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

#print(polarity)
        
######################################
# print sentiment pie chart
# ###################################        

labels = 'Positive sentiment', 'Negative sentiment', 'Neutral sentiment'
sizes = [positive, negative, neutral]
frequencies = [x/numTweets for x in sizes]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#explode = (0.1, 0, 0, 0)  # explode 1st slice
# Plot
plt.pie(sizes, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Percentage of Tweets with a certain sentiment')
plt.show()



###########################################
#most used hashtag if sentiment is negative
###########################################
def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    if tweet_analysis.polarity > 0:
        return 'positive'

    elif tweet_analysis.polarity == 0:
        return 'neutral'

    else:
        return 'negative'

my_tweets.rewind()
hashList = []
for tweet in my_tweets:
                for e in t['entities']['hashtags']:
                        h = e['text']
                        if tweet_sentiment(tweet['text']) == 'negative':
                                hashList.append(h)
D = Counter(hashList)
subset = dict(D.most_common(15))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))

pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align = 'center', color = 'yellowgreen')
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('Top 15 of hashtags captured, negative')
plt.tight_layout()
plt.show()



###########################################
#most used hashtag if sentiment is positive
###########################################
my_tweets.rewind()

def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    if tweet_analysis.polarity > 0:
        return 'positive'

    elif tweet_analysis.polarity == 0:
        return 'neutral'

    else:
        return 'negative'


hashList = []
for tweet in my_tweets:
        for e in t['entities']['hashtags']:
                h = e['text']
                if tweet_sentiment(tweet['text']) == 'positive':
                                hashList.append(h)
D = Counter(hashList)
subset = dict(D.most_common(15))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))

pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align = 'center', color = 'yellowgreen')
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('Top 15 of hashtags captured, positive')
plt.tight_layout()
plt.show()

