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
place_types = []



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
    place_type = i['place_type']
    place_types.append(place_type)


#group by
m = pd.DataFrame({'country': countries, 'city': cities})
count = m.groupby(['city']).size().to_frame('count').reset_index()
ordered_count = count.sort_values(by=['count'])
count_list = ordered_count.astype({'count': int})

my_tweets.rewind()
print(count_list[-20:])
print(len(location))


#list with us tweets
na_tweets = []
eu_tweets = []



# for i in my_tweets:
#     if i['place']  == "Canada":
#             us_tweets.append(i['text'])
#     else:
#         us_tweets.append("")
   
#place type

for i in location:
    if i['country'] == "United States" or i['country'] == "Canada":
        na_tweets.append(i['id'])

for i in location:
    if i['country'] == "Germany" or i['country'] == "Ireland" or i['country'] == "United Kingdom" or i['country'] == "France" or i['country'] == "Portugal" or i['country'] == "Deutschland" or i['country'] == "España" or i['country'] == "Sverige" or i['country'] == "Sweden" or i['country'] == "The Netherlands" or i['country'] == "Turkey" or i['country'] == "Norway" or i['country'] == "Nederland" or i['country'] == "Italie" or i['country'] == "Norge" or i['country'] == "Grèce" or i['country'] == "Armenia": 
        eu_tweets.append(i['id'])

#dataframe = pd.DataFrame(index = id, data = {"text": my_tweets['text'], "na": na_tweets}) 
