# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:23:28 2019

@author: admin
"""

# importing googlemaps module 
import googlemaps 
  


####################################

gmaps = googlemaps.Client(key='AIzaSyBV6DUemlJVqGRe8dZ_Bc2BPSSOctBJZO4')

origins = '19 Forest St, Cambridge, MA 02140'

destinations = 'Wayfair, Copley Place 7th floor, Boston, MA'

mode = 'transit'

arrival_time = datetime.datetime(2019,7,29,9,15)

transit_mode= ["train", "tram", "subway"]

transit_routing_preference= 'fewer_transfers'

traffic_model = "best_guess"

A = gmaps.distance_matrix(origins, destinations,
                    mode, language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=arrival_time, transit_mode=transit_mode,
                    transit_routing_preference=transit_routing_preference, traffic_model=traffic_model, region=None)

print(A)

distance = A['rows'][0]['elements'][0]['distance']['value']

duration = A['rows'][0]['elements'][0]['duration']['value']


df['distance'] = 0
df['duration'] = 0

position = 0
for origins in df['address']:
    
    
    
    
    distance = A['rows'][0]['elements'][0]['distance']['value']
    duration = A['rows'][0]['elements'][0]['duration']['value']
    
    
    df['distance'].iloc[i] = distance
    df['duration'].iloc[i] = duration
    position += 1
    
    









#departure_time= 'arrival_time=' + 'MONDAY 9 AM' + '&'





units= 'units="' + 'imperial' + '"&'

