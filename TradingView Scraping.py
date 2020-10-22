# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:50:00 2019

@author: admin
"""
import json 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd  
from datetime import datetime 
import time
import numpy as np
import re
import sys
from bs4 import BeautifulSoup
import requests

def convert_epoch(value):
    date = datetime.fromtimestamp(value).strftime('%Y-%m-%d')
    return date

Ticker = 'USDEUR'

# Create the view
def get_big_chart(Ticker):
    # Open browser
    driver = webdriver.Chrome()
    driver.get('https://www.tradingview.com/') 
    time.sleep(1)
    # Open basic chart
    driver.find_element_by_name('query').send_keys('')
    driver.find_element_by_name('query').send_keys(Ticker,Keys.ENTER)           
    time.sleep(1)
    # Open detailed chart
    act_url = driver.current_url
    new_url = act_url.replace('symbols/','chart?symbol=').replace('-','%3A')[:-1]
    driver.quit()
    return new_url


def get_fixed_url(new_url):
    driver = webdriver.Chrome()
    driver.get(new_url)
    driver.maximize_window()
    time.sleep(3)
     # 1 YEAR DATAFRAME
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[7]/div').click()
    # Locating button
    actions = ActionChains(driver)
    element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[16]')
    actions.move_to_element_with_offset(element,50,0)
    actions.click()
    actions.perform()
    actions.reset_actions()   
    time.sleep(1)
    # Logging in              
    xpath = '//*[@id="signin-form"]/div[1]/div[1]/input'
    driver.find_element_by_xpath(xpath).send_keys('juanjchamie@gmail.com')
    time.sleep(1)
    xpath = '//*[@id="signin-form"]/div[2]/div[1]/div[1]/input'
    driver.find_element_by_xpath(xpath).send_keys('IL2bQK88.',Keys.ENTER)   
    # Creating static Chart (PUBLISH)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[1]/div[1]/div/div/div/input').send_keys('Test1')
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[1]/div[2]/div[2]/textarea').send_keys('Test1')       
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/label/div[1]').click()
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/div/div/div[1]/div/span/span[2]/label/span').click()
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/button[2]/span[2]').click()      
    driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[2]/div/div/button[2]/span[2]').click()
    time.sleep(1) 
    # Changing tab
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    url = driver.current_url
    while driver.current_url == 'https://www.tradingview.com/loading/':
        time.sleep(2)
        url = driver.current_url
    driver.quit()
    return url


def reading_from_final_url(final_url):
    result = requests.get(final_url)
    src = result.content
    soupX = BeautifulSoup(src, 'lxml')      
    soup = soupX.find('div', attrs={'class':'tv-chart-view js-chart-view'})['data-options']
    res = json.loads(soup) 
    res0 = json.loads(res['content'])['panes'][0]['sources'][0]['bars']['data']    
    df = pd.DataFrame(columns=['date','close'])
    i = 0
    for data_point in res0:
        
        d = data_point['value'][0] 
        c = data_point['value'][4]
        df.loc[i,'date'] = d
        df.loc[i,'close'] = c
        i += 1
    df['date'] = df['date'].apply(convert_epoch)    
    return df

def delete_last_chart():
    driver = webdriver.Chrome()
    driver.get('https://www.tradingview.com/u/JQ-dev/#published-charts') 
    time.sleep(3) 
    
    xpath = '/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/a'
    driver.find_element_by_xpath(xpath).click()     
    
    xpath = '//*[@id="signin-form"]/div[1]/div[1]/input'
    driver.find_element_by_xpath(xpath).send_keys('juanjchamie@gmail.com')
    time.sleep(1)
    xpath = '//*[@id="signin-form"]/div[2]/div[1]/div[1]/input'
    driver.find_element_by_xpath(xpath).send_keys('IL2bQK88.',Keys.ENTER)     
    
    xpath = '/html/body/div[3]/div[4]/div[5]/div/div[1]/div/div/div/div[1]/div/div[1]/a'
    driver.find_element_by_xpath(xpath).click() 
    time.sleep(1) 
    xpath ='//*[@id="overlap-manager-root"]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[3]/div/span[1]'
    driver.find_element_by_xpath(xpath).click() 
    time.sleep(1) 
    xpath ='//*[@id="overlap-manager-root"]/div[2]/div[2]/div/div/div/div[3]/div[2]/span[2]'
    driver.find_element_by_xpath(xpath).click() 
    time.sleep(1) 
    driver.quit()
    return print('done')


Ticker = 'USDGBP'

new_url = get_big_chart(Ticker)

final_url = get_fixed_url(new_url)

df = reading_from_final_url(url)

delete_last_chart()






