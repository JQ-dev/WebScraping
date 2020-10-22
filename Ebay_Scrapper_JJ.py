# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:18:21 2019

@author: admin
"""

from bs4 import BeautifulSoup 
import pandas as pd
#from selenium import webdriver
import requests
import re
from datetime import datetime, time, timedelta


def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


def one_page(big_box,inside_data,url):
    page = pd.DataFrame()
    count = 0
    result = requests.get(url)
    src = result.content
    soupX = BeautifulSoup(src, 'lxml')      
    for box in eval( big_box):   
        for field in inside_data:
            try:
                page.loc[count,field[0]] = eval( 'box' +  field[1] )
            except:
                page.loc[count,field[0]] = 'N/A'
        count += 1  
    return(page)



def scrap_once(url,pages,inside_data,big_box): 
    try:         
        df = pd.DataFrame()         
        page = 1            
        for i in range(pages):      
            temp = one_page(big_box,inside_data,url)
            df = df.append(temp)      
            page += 1 
            url = url[:-1] + str(page)                     
        df['value'] = df['value'].replace('\$','',regex=True).replace(',','',regex=True).apply(float)
        df['time_left'] = df['time_left'].replace(' left','',regex=True).replace('d','*86400',regex=True).replace('h','*3600',regex=True).replace('m','*60',regex=True).replace('s','',regex=True).replace(' ','+',regex=True)
        df['seconds_left'] = df['time_left'].apply(eval)
        df['time_left'] = df['seconds_left'].apply(lambda x : str(timedelta(seconds = x)))
        df['shipping'] = df['shipping'].replace('Free Shipping','0').replace('shipping','',regex=True).replace('\+\$','',regex=True).replace(',','',regex=True).replace('N/A','999',regex=True)
        df['shipping'] = df['shipping'].apply(float)
        df['num_bids'] = df['num_bids'].replace('bids','',regex=True).replace('bid','',regex=True).apply(int)
        df['auction_end_day'] = df['seconds_left'].apply(lambda x : datetime.now() - timedelta(seconds=x) ).apply( lambda x : x.strftime('%A') )
        df['auction_end_hour'] = df['seconds_left'].apply(lambda x : datetime.now() - timedelta(seconds=x) ).apply( lambda x : x.strftime('%H') )
        df['log'] = datetime.now()            
        return(df)        
    except:
         return(df)  



big_box = '''soupX.findAll('div', attrs={'class': re.compile('^s-item__wrapper ')})'''

inside_data = []
inside_data.append( ['title'     , '''.find('h3', attrs={'class': 's-item__title'}).text.strip()'''] )
inside_data.append( ['condition' , '''.find('span', attrs={'class': 'SECONDARY_INFO'}).text.strip()'''] )
inside_data.append( ['value'     , '''.find('span', attrs={'class': 's-item__price'}).text.strip()'''] )
inside_data.append( ['time_left' , '''.find('span', attrs={'class': 's-item__time-left'}).text.strip()'''] )
inside_data.append( ['shipping'  , '''.find('span', attrs={'class': 's-item__shipping s-item__logisticsCost'}).text.strip()'''] )
inside_data.append( ['num_bids'  , '''.find('span', attrs={'class': 's-item__bids s-item__bidCount'}).text.strip()'''] )
inside_data.append( ['link'      , '''.find('a')['href']'''] )

#product = 'macbook+air'
#year = '2017'

#url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='+ product +'&LH_TitleDesc=0&_sacat=111422&Release%2520Year='+ year +'&_oaa=1&_fsrp=1&_dcat=111422&LH_Auction=1&_sop=1&_pgn=1'
url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=macbook+air&LH_TitleDesc=0&_sacat=111422&_oaa=1&_fsrp=1&LH_Auction=1&_sop=1&_ipg=200&_oaa=1&_dcat=111422&_pgn=1'
pages = 2
#del(product,year)


times = 400

dfXX = pd.DataFrame()  

for i in range(times):
    try:
        df = scrap_once(url,pages,inside_data,big_box)      
        df['real_time_left'] = df['time_left'] 
      
        dfXX = dfXX.append(df)
        dfXX['real_time_left'] = dfXX['seconds_left'] - (( datetime.now() - dfXX['log'] ).apply( lambda x : x.seconds )) 
        dfXX['real_time_left'] = dfXX['real_time_left'].apply( lambda x : max(0,x))              
        # Removing duplicates
        dfXX = dfXX.sort_values("log", ascending=False)
        dfXX = dfXX.drop_duplicates(['link','num_bids'])
      
        closest = df.loc[:,'seconds_left'].min()
        next_iteration = 600
        if closest < 1800:
            next_iteration = 300
        if closest < 900:
            next_iteration = 60     
     
        dfXX.to_csv('Auctions_Ebay_MacbookAir4.csv',sep=',',na_rep='N/D')
        
        print('The last {1} was the {0:%d} of {0:%B} at {0:%I:%M%p}.'.format(datetime.now(),'iteration'))
        print(i,'of 300. And the next one will be after:' , next_iteration/60 , 'minutes')    
        
    except:
        continue
    sleep(next_iteration)
           




