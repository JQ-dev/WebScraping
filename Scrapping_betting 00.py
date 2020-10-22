# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 11:32:07 2019

@author: admin
"""

# pip install beautifulsoup4
# pip install requests
# pip install selenium

from bs4 import BeautifulSoup
#import requests   
from selenium import webdriver
import pandas as pd  
from datetime import datetime
import time
import numpy as np




def Bundesliga():

    odds_table = pd.DataFrame()
    
    url = "https://sports.bwin.com/en/sports#categoryIds=25,1230&eventId=&leagueIds=43&marketGroupId=&orderMode=Event&page=0&sportId=4&templateIds=0.9060810013218714"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
        
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    containers1 = soup.find_all("table", {"class": "marketboard-event-without-header__markets-list"})
    containers2 = soup.find_all("table", {"class": "marketboard-event-with-header__markets-list"})

    resultAndOdds = []    
    for container in containers1:
        divs = container.findAll('div')
        texts = [div.text for div in divs]
        it = iter(texts)
        resultAndOdds.append(list(zip(it, it)))
    
    for container in containers2:
        divs = container.findAll('div')
        texts = [div.text for div in divs]
        it = iter(texts)
        resultAndOdds.append(list(zip(it, it)))

    new_set = pd.DataFrame()
    for i in range(9):  
        new_set.loc[i,'local'] = resultAndOdds[i][0][1]
        new_set.loc[i,'visitor'] = resultAndOdds[i][3][0]
        new_set.loc[i,'L'] = resultAndOdds[i][1][0]
        new_set.loc[i,'T'] = resultAndOdds[i][2][0]
        new_set.loc[i,'V'] = resultAndOdds[i][3][1]  
    
        j = i*3 + 18
        new_set.loc[i,'more 1 half'] = resultAndOdds[j][0][1]
        new_set.loc[i,'same amount'] = resultAndOdds[j][1][1]
        new_set.loc[i,'more 2 half'] = resultAndOdds[j][2][1]
        new_set.loc[i,'L more 1 half'] = resultAndOdds[j+1][0][1]
        new_set.loc[i,'L same amount'] = resultAndOdds[j+1][1][1]
        new_set.loc[i,'L more 2 half'] = resultAndOdds[j+1][2][1]
        new_set.loc[i,'V more 1 half'] = resultAndOdds[j+2][0][1]
        new_set.loc[i,'V same amount'] = resultAndOdds[j+2][1][1]
        new_set.loc[i,'V more 2 half'] = resultAndOdds[j+2][2][1]   
            
    for i in range(9,18):  
        new_set.loc[i,'local'] = resultAndOdds[i][0][1]
        new_set.loc[i,'visitor'] = resultAndOdds[i][3][0]
        new_set.loc[i,'L'] = resultAndOdds[i][1][0]
        new_set.loc[i,'T'] = resultAndOdds[i][2][0]
        new_set.loc[i,'V'] = resultAndOdds[i][3][1]  
     
    for i in range(2,14):
        values = new_set.iloc[:,i].fillna(-1).apply(int)
        cond = values > 0
        new_set.iloc[:,i] = ((values+100)/100).where(cond,(1-(100/values))).round(2).replace(101,np.nan)
    
    new_set['Fairness'] = (1/new_set['L'])+(1/new_set['T'])+(1/new_set['V'])

    new_set['date_time'] = now
    
    odds_table = odds_table.append(new_set)

    driver.close()
    return(odds_table)





Busdesliga = pd.DataFrame()

while True:
    table = Bundesliga()
    Busdesliga = Busdesliga.append(table)
    print(datetime.now().strftime('%Y-%m-%d %H:%M'))
    time.sleep(3600)

# 6 15 pm




  
    