# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:18:21 2019

@author: admin
"""

from bs4 import BeautifulSoup 
#import re
import pandas as pd
import numpy as np
#from selenium import webdriver
import requests
import re
from datetime import datetime, time, timedelta
import time
import googlemaps 



def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


def get_the_soup(url):
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }    
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)                
    soup = BeautifulSoup(r.content, 'lxml')    
    return (soup)


def one_page(big_box,inside_data,url):
    output = pd.DataFrame()
    soupX = get_the_soup(url) 
    box = eval(big_box)
    iter_box = box.findAll('article')
    count = 0    
    
    for internal_box in iter_box:   
        try:
            for field in inside_data:
                try:
                    output.loc[count,field[0]] = eval( 'internal_box' +  field[1] )
                except:
                    output.loc[count,field[0]] = 'N/A'    
            count += 1      
        except:
            continue     
    return(output)



def scrap_once(url,pages,inside_data,big_box):  
    try:         
        df = pd.DataFrame()   
        
        page = 1  
        page_number = 1          
        for i in range(pages):      
            temp = one_page(big_box,inside_data,url)
            temp['page_number'] = page_number
            df = df.append(temp)      
            page += 1 
            old_text = '{%22currentPage%22:' + str(page-1) + '}' 
            new_text = '{%22currentPage%22:' + str(page) + '}'
            url = url.replace(old_text, new_text )
            page_number += 1                                  
        return(df)      
    except:
         return(df)  


#df_final = new_df.copy()

def clean_data(df_final):

    df_final.loc[:,'details'] = (df_final.loc[:,'details'].replace(' bds','_bds',regex=True)
                                                        .replace(' sqft','_sqft',regex=True)
                                                        .replace(' ba','_ba',regex=True)
                                                        .replace('bds','bds,',regex=True)
                                                        .replace('ba','ba,',regex=True)    )                          
                                          
    cond = df_final['details'].str.contains('\$',regex=True)                        
    df_final.loc[:,'details'] = df_final.loc[:,'details'].where(cond,('$+ ' + df_final['details']))    
    cond = df_final['details'].str[-4:]  == 'bds,'
    df_final.loc[:,'details'] = (df_final.loc[:,'details'] + '1_ba,').where(cond,df_final.loc[:,'details'])    
    df_final.loc[:,'details'] = df_final.loc[:,'details'].replace('-','',regex=True)    

    df_final[['price2','details','more']] = df_final.details.str.split(" ",n=2,expand=True,)   
    df_final = df_final.drop('more',axis=1)
    
#    cond = df_final['details'].str[-1:]  == ','
#    df_final.loc[:,'details'] = (df_final.loc[:,'details'] + '_sqft').where(cond,df_final.loc[:,'details'])
    
    df_final.loc[:,'details'] = (df_final.loc[:,'details'].replace('1,','1',regex=True).replace('2,','2',regex=True)
        .replace('3,','3',regex=True).replace('4,','4',regex=True).replace('5,','5',regex=True).replace('6,','6',regex=True)
        .replace('7,','7',regex=True).replace('8,','8',regex=True).replace('6,','6',regex=True).replace('7,','7',regex=True)
        .replace('8,','8',regex=True).replace('9,','9',regex=True).replace('0,','0',regex=True)                    )
        
    df_final[['beds','A','bath','C','sqft']] = df_final.details.str.split(",",n=4,expand=True)  
    df_final = df_final.drop(['A','C'],axis=1)
    df_final.loc[:,'beds'] = df_final.loc[:,'beds'].replace('_bds','',regex=True).fillna(np.nan).apply(int).replace(0,np.nan)    
    df_final.loc[:,'bath'] = df_final.loc[:,'bath'].replace('_ba','',regex=True).fillna(np.nan).replace('','0',regex=True).replace('\$','0',regex=True).replace('\+','0',regex=True).apply(float).replace(0,np.nan)    
    df_final.loc[:,'sqft'] = df_final.loc[:,'sqft'].replace('_sqft','',regex=True).replace('','0',regex=True).fillna(np.nan).apply(float).replace(0,np.nan)
    
    
    df_final.loc[:,'price'] = (df_final.loc[:,'price'].replace('\$','',regex=True).replace('/mo','',regex=True)
                            .replace('\+','',regex=True).replace(',','',regex=True).replace('--','',regex=True) 
                            .replace('', 0).replace('N/A',0).fillna(0).apply(int).replace(0,np.nan)      )  
    
    df_final.loc[:,'price2'] = (df_final.loc[:,'price2'].replace('\$','',regex=True).replace('\+','',regex=True).replace(',','',regex=True)
                            .replace('--','',regex=True).fillna(0).replace('', 0).replace('N/A',0)
                            .apply(int).replace(0,np.nan)   )
                   
    cond = df_final.loc[:,'price'].isna() 
    df_final.loc[:,'price'] = df_final.loc[:,'price2'].where(cond,df_final.loc[:,'price'])
    
    df_final = df_final.drop(['price2','details'],axis=1)
    
    return (df_final)




def google_addresses(df):

    df = df.loc[:,'address'].drop_duplicates().replace('\(undisclosed Address\), ', '',regex=True)
    df = pd.DataFrame(df)
    
    df['distance_km'] = 0
    df['distance_m'] = 0
    df['duration_min'] = 0
    df['duration_sec'] = 0    
           
    ###############################
    gmaps = googlemaps.Client(key='AIzaSyBV6DUemlJVqGRe8dZ_Bc2BPSSOctBJZO4')
    origins = '19 Forest St, Cambridge, MA 02140'
    destinations = 'Wayfair, Copley Place 7th floor, Boston, MA'
    mode = 'transit'
    arrival_time = datetime(2019,8,26,9,15)
    transit_mode= ["train", "tram", "subway"]
    transit_routing_preference= 'fewer_transfers'
    traffic_model = "best_guess"
    ###############################    
        

#     groups of 25
#    units_per_group = 25
#    total = len( df['address'] )
#    groups = int(np.ceil(len( df['address'])/25))
#    groups_list = []
#    
#    for group in range(groups):
#        pos_list = list( range( units_per_group * group , min(units_per_group*(group+1),total) ) )
#        groups_list.append(pos_list)
#    
#    del(units_per_group,total,groups,pos_list,group)
#    
#    for test in groups_list:
#        origins = list(df.loc[:,'address'].iloc[test])

    position = 0
    for origins in df['address']:    
        try:        
            A = gmaps.distance_matrix(origins, destinations,
                            mode, language=None, avoid=None, units=None,
                            departure_time=None, arrival_time=arrival_time, transit_mode=transit_mode,
                            transit_routing_preference=transit_routing_preference, traffic_model=traffic_model, region=None)
            
            distanceK = A['rows'][0]['elements'][0]['distance']['text']
            durationM = A['rows'][0]['elements'][0]['duration']['text']
            distanceM = A['rows'][0]['elements'][0]['distance']['value']
            durationS = A['rows'][0]['elements'][0]['duration']['value']        
            
            df.loc[:,'distance_km'].iloc[position] = distanceK
            df.loc[:,'duration_min'].iloc[position] = durationM
            df.loc[:,'distance_m'].iloc[position] = distanceM
            df.loc[:,'duration_sec'].iloc[position] = durationS     
       
        except:        
            df.loc[:,'distance_km'].iloc[position] = 'N/A'
            df.loc[:,'duration_min'].iloc[position] = 'N/A'   
            df.loc[:,'duration_min'].iloc[position] = 'N/A'
            df.loc[:,'duration_min'].iloc[position] = 'N/A'          
            
        position += 1    
 
    return(df)
    (df_final)




############################################################################################################################
############################################################################################################################
############################################################################################################################
############################################################################################################################
############################################################################################################################

big_box = '''soupX.find('ul', attrs={'class': re.compile('^photo-cards photo-cards_wow')})'''

inside_data = []
inside_data.append( ['address' , '''.find('h3', attrs={'class': 'list-card-addr'}).text.strip()'''] )
inside_data.append( ['price'   , '''.find('div', attrs={'class': 'list-card-price'}).text.strip()'''] )
inside_data.append( ['type'    , '''.find('div', attrs={'class': 'list-card-type'}).text.strip()'''] )
inside_data.append( ['ad_time' , '''.find('div', attrs={'class': 'list-card-variable-text list-card-img-overlay'}).text.strip()'''] )
inside_data.append( ['link'    , '''.find('a')['href']'''] )
inside_data.append( ['details' , '''.find('ul', attrs={'class': 'list-card-details'}).text'''] )


url = 'https://www.zillow.com/homes/for_rent/2-_beds/2_p/?searchQueryState={%22pagination%22:{%22currentPage%22:1},%22mapBounds%22:{%22west%22:-71.33241593875925,%22east%22:-70.79271256961863,%22south%22:42.17162178739379,%22north%22:42.488579602398794},%22usersSearchTerm%22:%22Boston%22,%22isMapVisible%22:true,%22mapZoom%22:11,%22filterState%22:{%22sortSelection%22:{%22value%22:%22days%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isForRent%22:{%22value%22:true},%22monthlyPayment%22:{%22max%22:2600,%22min%22:1900},%22price%22:{%22max%22:702974,%22min%22:513712},%22beds%22:{%22min%22:2},%22doz%22:{%22value%22:%2214%22}},%22isListVisible%22:true}'

pages = 50


#########################
#########################

# UPDATE DATABASE
 
# Reading the actual
#        df_final = pd.read_csv('Zillow_V2.csv' )
#        
#        df_final.loc[:,'price'] = df_final.loc[:,'price'].replace('N/D','',regex=True).replace('\.0','',regex=True).replace('', 0).fillna(0).apply(int).replace(0,np.nan)
#        df_final.loc[:,'sqft'] = df_final.loc[:,'sqft'].replace('N/D','',regex=True).replace('\.0','',regex=True).replace('', 0).fillna(0).apply(int).replace(0,np.nan)
#        df_final.loc[:,'bath'] = df_final.loc[:,'bath'].replace('N/D','',regex=True).replace('', 0).apply(float).replace(0,np.nan)
#        
#        df_final = df_final.drop_duplicates(['address','price'])
#        df_final['sec'] = 0

# New scraping    
new_df = scrap_once(url,pages,inside_data,big_box)
new_df['address'] = new_df['address'].replace('\(undisclosed Address\), ', '',regex=True)

# Cleaning the new
new_df = clean_data(new_df)
new_df = new_df.drop_duplicates(['address','price'])
new_df['sec'] = 1

# Apending data - data frame to fill with distances at the end
#df_new_final = ( df_final.append(new_df,sort=True).sort_values('sec',ascending=True)
#                        .drop_duplicates(['address','price'])  )


# New address 124 - 447 / 124 - 

google_address = pd.read_csv('Address_and_distance2.csv')

address_needed = df_new_final.drop( list(google_address.columns[1:]) ,axis=1).drop_duplicates('address')
address_needed =  pd.merge(address_needed, google_address, how='left', on='address',validate='many_to_one')
address_needed = address_needed.loc[ address_needed['distance_km'].isna() ,:]


if len(address_needed['address']) > 0:
    new_addresses = google_addresses(address_needed)
    google_address = pd.concat([google_address,new_addresses]) #.drop_duplicates('address')
    google_address.to_csv('Address_and_distance2.csv',sep=',',na_rep='N/D',index=False)   

#A = pd.concat([google_address,new_addresses]).drop_duplicates('address')
# Fill the data frame
# Joining tables

df_new_final = ( df_final.append(new_df,sort=True).sort_values('sec',ascending=False)
                        .drop_duplicates(['address','price'])  )

df_new_final = df_new_final.drop( list(google_address.columns[1:]) ,axis=1)

df_new_final =  pd.merge(df_new_final, google_address, how='left', on='address',validate='many_to_one')

# Update the version and save the file
df_new_final.to_csv('Zillow_V2.csv',sep=',',na_rep='N/D',index=False)   


