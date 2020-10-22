# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:18:21 2019

@author: admin
"""

from bs4 import BeautifulSoup 
import re
import pandas as pd
#from selenium import webdriver
import requests



def one_page(soupX):
    job_page = pd.DataFrame()
    count = 0
    for job in soupX.findAll('div', attrs={'class': re.compile('^jobsearch-SerpJobCard ')}):   
        try:
            job_page.loc[count,'title'] = job.find('a')['title']
        except:
            job_page.loc[count,'title'] = 'N/A'    
        try:
            job_page.loc[count,'company'] = job.find('span', attrs={'class': 'company'}).find('a').text.strip()
        except:
            job_page.loc[count,'company'] = job.find('span', attrs={'class': 'company'}).text.strip()     
        try:
            job_page.loc[count,'location'] = job.find('span', attrs={'class': 'location'}).text.strip()
        except:
            job_page.loc[count,'location'] = job.find('div', attrs={'class': 'location'}).text.strip()   
        try:
            job_page.loc[count,'summary'] = job.find('div', attrs={'class': 'summary'}).text.strip()
        except:
            job_page.loc[count,'summary'] = 'N/A'     
        try:
            job_page.loc[count,'salary'] = job.find('span', attrs={'class': 'salary no-wrap'}).text.strip()
        except:
            job_page.loc[count,'salary'] = 'N/A'     
        try:
            job_page.loc[count,'link'] = 'https://www.indeed.com' + job.find('a')['href']
        except:
            job_page.loc[count,'link'] = 'N/A'     
        count += 1   
    return(job_page)

#url2 = job_listing.loc[:,'link'].iloc[2]   

#def job_description(url2):
#    result2 = requests.get(url2)
#    src = result.content
#    soupX2 = BeautifulSoup(src, 'lxml') 
#    
#    description = soupX2.find('div', attrs={'class': 'jobsearch-ViewJobLayout   jobsearch-ViewJobLayout-changeTextSize jobsearch-ViewJobLayout-changeTextColor '} ).text.strip()

# jobsearch-ViewJobLayout   jobsearch-ViewJobLayout-changeTextSize jobsearch-ViewJobLayout-changeTextColor 

position = 'senior business analyst'
place = 'Boston,+MA'
min_salary = ''
pages = 200


url = 'https://www.indeed.com/jobs?q='+ position + min_salary + '&l=' + place + '&start=000'

job_listing = pd.DataFrame()


for i in range(pages):
    
    result = requests.get(url)
    src = result.content
    soupX = BeautifulSoup(src, 'lxml')  

    temp_listing = one_page(soupX)

    job_listing = job_listing.append(temp_listing)

    last3 = str(int(url[-3:])+20)
    if len(last3)==2:
        last3 = '0'+last3
    
    url = url[:-3]+last3


job_listing2  = job_listing.drop_duplicates(['company','title'])

companies = job_listing.loc[:,('company','location')].drop_duplicates()

job_listing.loc[:,'company'] = job_listing.loc[:,'company'].replace


del last3,i,min_salary,pages,place,temp_listing,url,position




