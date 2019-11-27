from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib import ticker
from collections import Counter
import numpy as np
import operator
import seaborn as sns
import pandas as pd
import cartopy

#import gmplot



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


location = []


for i in my_tweets:
    if i['place'] != None:
        loc = i['place']['bounding_box']['coordinates']
        location.append(loc)
    
#for i in location:
 #       location2.append({'full_name':location})

#print(*location, sep='\n')

#coordinates are 4 values if its a 'twitter place' --> pick the first
coordinates = []

#list of latitudes
latitude_list = []
longitude_list = []

for i in location:
    first = i[0][0]
    coordinates.append(first)
    

for i in coordinates:
    longitude = i[1]
    latitude = i[0]
    latitude_list.append(latitude)
    longitude_list.append(longitude)


#print(coordinates)


#fig = gmaps.figure(map_type='HYBRID')
#heatmap_layer = gmaps.heatmap_layer(coordinates)
#fig.add_layer(heatmap_layer)
#fig

# 1. Draw the map background
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=-119,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

# 2. scatter city data, with color reflecting population
# and size reflecting area
m.scatter(longitude, latitude, latlon=True, cmap='Reds', alpha=0.5)



#api key google, places: AIzaSyAjZWHtwxWWlHfJPODzbF8JAMaa5EVN9Kw
