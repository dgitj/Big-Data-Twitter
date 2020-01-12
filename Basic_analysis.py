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

my_tweets = db.twitterBrazil.find({},{'lang':1, '_id':0, 'id':1, 'text':1, 'entities.hashtags':1, 'geo':1, 'location':1, 'coordinates':1, 'place':1,
'in_reply_to_status_id':1, 'is_quote_status':1, 'retweeted_status':1, 'user.screen_name':1} )


location = []

for i in my_tweets:
    if i['place'] != None:
        loc = i['place']['bounding_box']['coordinates']
        location.append(loc)


print(len(location))
