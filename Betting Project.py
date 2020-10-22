# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 08:51:35 2019

BETS PROJECT !!!
BOVADA
@author: admin
"""

from bs4 import BeautifulSoup 
import pandas as pd
from selenium import webdriver
import time


def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

def one_scrapping(url):
    result = pd.DataFrame(columns=['teams','odds','date','log_time','url','link'])    
    driver = webdriver.Chrome()    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    big_box = soup.find_all('section', attrs={'class':'coupon-content'})
    row = 0
    for box in big_box:   
        try:
            result.loc[row,'date'] = box.find('span', attrs={'class': 'period hidden-xs'}).text.strip()
        except:
            result.loc[row,'date'] = 'N/A'
        try:
            result.loc[row,'link'] = box.find('a', attrs={'class': 'game-view-cta'})['href']
        except:
            result.loc[row,'link'] = 'N/A'            
        try:
            teams = box.find_all('h4', attrs={'class': 'competitor-name'})
            team_list = []
            for team in teams:
                team_list.append( team.find('span', attrs={'class' :'name'}).text.strip() )
            result.loc[row,'teams'] = team_list  
        except:
            result.loc[row,'teams'] = 'N/A'             
        try:
            odds = box.find_all('sp-three-way-vertical', attrs={'class': 'market-type'})
            odd_list = []
            for odd in odds:
                odd_list.append( odd.find('span', attrs={'class' :'bet-price'}).text.strip() )
            result.loc[row,'odds'] = odd_list  
        except:
            result.loc[row,'odds'] = 'N/A'                      
        row += 1
    result.loc[:,'log_time'] =  time.strftime("%m/%d/%y %I:%M %p")
    result.loc[:,'url'] =  url
    return(result)



def soccer_bovada(url_list, wait): 
    frecuency = wait 
    while True:
        recent_combined = pd.DataFrame()
        for url in url_list:
            most_recent = one_scrapping(url)
            try:
                data_base = data_base.append(most_recent) 
            except:
                data_base = most_recent.copy()
            recent_combined = recent_combined.append(most_recent) 
            del most_recent   
        data_base.to_csv('soccer.csv',sep=',',na_rep='N/D')
        recent_combined.to_csv('soccer_temp.csv',sep=',',na_rep='N/D')
        sleep(frecuency)    


#########################################################################################################################

url_list = ['https://www.bovada.lv/sports/baseball/mlb',
            'https://www.bovada.lv/sports/soccer/south-america/brazil/serie-a',
            'https://www.bovada.lv/sports/soccer/england-premier-league',
            'https://www.bovada.lv/sports/soccer/spain-la-liga',
            'https://www.bovada.lv/sports/soccer/germany-bundesliga']

wait = 300

soccer_bovada(url_list, wait)



