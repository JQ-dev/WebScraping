# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:24:38 2019


"""
  
from selenium import webdriver
import pandas as pd  
import numpy as np


df_zillow = pd.read_csv('Zillow_V2.csv' )


# Min Requeriments

# Prices from 1800 and time up to several hours
price_max = 2600
price_min = 2300 
time_to_work_max = 45
time_to_work_min = 0
city =  ''
update = 'hours ago'
# yesterday - hours ago - 1 day ago - days ago
last_search = True

df_zillow.loc[:,'price'] = df_zillow.loc[:,'price'].replace('N/D','',regex=True).replace('\.0','',regex=True).replace('', 0).fillna(0).apply(int).replace(0,np.nan)
df_zillow.loc[:,'sqft'] = df_zillow.loc[:,'sqft'].replace('N/D','',regex=True).replace('\.0','',regex=True).replace('', 0).fillna(0).apply(int).replace(0,np.nan)
df_zillow.loc[:,'bath'] = df_zillow.loc[:,'bath'].replace('N/D','',regex=True).replace('', 0).apply(float).replace(0,np.nan)

cond1 = df_zillow.loc[:,'price'] <= price_max
cond2 = df_zillow.loc[:,'price'] >= price_min
cond3 = df_zillow.loc[:,'duration_sec'] <= (time_to_work_max * 60)
cond4 = df_zillow.loc[:,'duration_sec'] >= (time_to_work_min * 60)
cond5 = df_zillow.loc[:,'address'].str.contains(city,regex=True) 
cond6 = df_zillow.loc[:,'ad_time'].str.contains(update,regex=True) 
cond7 = ( (df_zillow.loc[:,'sec'] == 1) if last_search else True)

    
filtered_links = df_zillow.loc[cond1&cond2&cond3&cond4&cond5&cond6&cond7,:]
del(cond1,cond2,cond3,cond4,cond5,cond6,cond7)
del(price_max,price_min,time_to_work_max,time_to_work_min,city,update,last_search)

# Open links


for link in filtered_links['link']:
    print(link)
    driver = webdriver.Chrome()
    driver.get(link)

del(link)






