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

####################################################
# Plot of Languages (autodetected by Twitter)
####################################################
langsList = []
for t in my_tweets:
	langsList.append(t['lang'])

D = Counter(langsList)
# ----------- Bar Plot ------------------------
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())
plt.title('Languages spoken in the tweets captured')
plt.show()

###################################################
#Re-Check twitter language detection
##################################################
from langdetect import detect
langsList2 = []

for t in my_tweets:
        langsList2.append(detect(t))

E = Counter(langsList2) 
                          
plt.bar(range(len(E)), E.values(), align='center')
plt.xticks(range(len(E)), E.keys())
plt.title('Languages spoken in the tweets captured2')
plt.show()


##############################################################
# Plot how many of them are retweets, replies,
# quotations or original tweets
##############################################################
my_tweets.rewind() #Reset cursor
retweets = 0
replies = 0
quotations = 0
originals = 0
for t in my_tweets:
	if t.get('retweeted_status') is not None:
		retweets=retweets+1
	elif t['is_quote_status'] is not False:
		quotations = quotations+1
	elif t.get('in_reply_to_status_id') is not None:
		replies = replies+1
	else:
		originals = originals+1

# ----------- Pie Chart ------------------------
labels = 'Original Content', 'Retweets', 'Quotations', 'Replies'
sizes = [originals, retweets, quotations, replies]
frequencies = [x/numTweets for x in sizes]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # explode 1st slice
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Percentage of Tweets depending on how the content is generated')
plt.show()


##################################################################
# Plot secondary hashtags
##################################################################
my_tweets.rewind()
hashList = []
for t in my_tweets:
    for e in t['entities']['hashtags']:
        h = e['text']
        hashList.append(h)
D = Counter(hashList)
subset = dict(D.most_common(15))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align = 'center', color = 'yellowgreen')
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('Top 15 of hashtags captured')
plt.tight_layout()
plt.show()



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


def tweet_sentiment(tweet):
    tweet_analysis = TextBlob(clean_tweet(tweet))
    if tweet_analysis.polarity > 0:
        return 'positive'

    elif tweet_analysis.polarity == 0:
        return 'neutral'

    else:
        return 'negative'

for tweet in my_tweets:
        print(tweet_sentiment(tweet['text']), " sentiment for the tweet: ", tweet['text'])
        if tweet_sentiment(tweet['text']) == 'positive':
                positive = positive+1;
                #print(tweet['text'] + "pos")

        if tweet_sentiment(tweet['text']) == 'neutral':
                neutral = neutral+1;
                #print(tweet['text'] + "neutral")

        if tweet_sentiment(tweet['text']) == 'negative':
                negative = negative+1;
                #print(tweet['text'] + "neg")


        

print(positive)
print(negative)
print(neutral)

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



                
        
      
