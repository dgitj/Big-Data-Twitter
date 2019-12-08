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
import six
import cartopy.crs as ccrs
from matplotlib.patches import Circle

from itertools import product





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

#sort and group by location 

m = pd.DataFrame({'longitude': longitude_list, 'latitude': latitude_list})
count = m.groupby(['longitude', 'latitude']).size().to_frame('count').reset_index()
ordered_count = count.sort_values(by=['count'])
count_list = ordered_count.astype({'count': int})



 
############################################
#plot map
############################################

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
# plot individual locations                                                                                                       
#ax.plot(latitude_list, longitude_list, 'ro', transform=ccrs.PlateCarree())

#radius
def get_radius(freq):
    if freq < 20:
        return 0.5
    elif freq < 100:
        return 2.0
    elif freq < 1000:
        return 1.8


# plot count of tweets per location
for i, row in count_list.iterrows():
    ax.add_patch(Circle(xy=[row[1], row[0]], radius=get_radius(row[2]), color='blue', alpha=0.6, transform=ccrs.PlateCarree()))
    
    

#api key google, places: AIzaSyAjZWHtwxWWlHfJPODzbF8JAMaa5EVN9Kw

plt.show()