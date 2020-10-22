# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:03:36 2019

@author: admin
"""

from bs4 import BeautifulSoup 
from selenium import webdriver
import requests
import pandas as pd  
#from datetime import datetime
#import time
#import numpy as np


# INDEED SCRAPER

url = 'https://www.indeed.com/jobs?q=analyst+$100,000&l=Boston,+MA&start=0'
result = requests.get(url)

print(result.status_code)
print(result.headers)

src = result.content
soup = BeautifulSoup(src, 'lxml')


def extract_job_title_from_result(soup): 
    jobs = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            jobs.append(a['title'])
    return(jobs)
  


def extract_company_from_result(soup): 
    companies = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)
 

#def extract_location_from_result(soup): 
#    locations = []
#    spans = soup.findAll('div', attrs={'class': 'data-rc-loc'})
#    for span in spans:
#        locations.append(span.text)
#    return(locations)
#
#extract_location_from_result(soup)


#def extract_salary_from_result(soup): 
#    salary = []
#    spans = soup.findAll('span', attrs={'class': 'salary no-wrap'})
#    for span in spans:
#        salary.append(span.text)
#    return(salary)
#
#extract_salary_from_result(soup)


#def extract_salary_from_result(soup): 
#    salaries = []
#    for div in soup.find_all(name='div', attrs={'class':'row'}):
#        try:
#            salaries.append(div.find('nobr').text)
#        except:
#            try:
#                div_two = div.find(name='div', attrs={'class':'sjcl'})
#                div_three = div_two.find('div')
#                salaries.append(div_three.text.strip())
#            except:
#                salaries.append('Nothing_found')
#    return(salaries)
#    
#    
#extract_salary_from_result(soup)


def extract_summary_from_result(soup): 
    summaries = []
    spans = soup.findAll('div', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)
 
    
    
def extract_dates_from_result(soup): 
    dates = []
    spans = soup.findAll('span', attrs={'class': 'date'})
    for span in spans:
        dates.append(span.text.strip())
    return(dates)    
    
    

    
    
url = 'https://www.indeed.com/jobs?q=analyst+$80,000&l=Boston,+MA&start=000'

url = 'https://www.indeed.com/jobs?q=data+scientis+$80,000&l=Boston,+MA&start=000'

job_listing80 = pd.DataFrame()

for i in range(10):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')  

    temp_listing = pd.DataFrame()  
    temp_listing['Job'] = extract_job_title_from_result(soup) 
    temp_listing['Company'] = extract_company_from_result(soup)
    temp_listing['Summary'] = extract_summary_from_result(soup)
#    temp_listing['date'] = extract_dates_from_result(soup)

    job_listing80 = job_listing80.append(temp_listing)

    last3 = str(int(url[-3:])+20)
    if len(last3)==2:
        last3 = '0'+last3
    
    url = url[:-3]+last3






  












#
#driver = webdriver.Chrome()
#driver.get(url)
#
#def get_soup(url):
#    driver = webdriver.Chrome()
#    driver.get(url)
#    html = driver.page_source
#    soup = BeautifulSoup(html, 'html.parser')
#    driver.close()
#    return soup
#
#def grab_job_links(soup):
#    urls = []
#    for link in soup.find_all('h2', {'class': 'jobtitle'}):
#        partial_url = link.a.get('href')
#        url = 'https://ca.indeed.com' + partial_url
#        urls.append(url)
#    return urls
#
#soup.find(name='div', attrs={'id':"searchCount"}).get_text()

#
#for i in range(2, num_pages+1):
#    num = (i-1) * 10
#    base_url = 'https://ca.indeed.com/jobs?q={}&l={}&start={}'.format(query, location, num)
#    try:
#        soup = get_soup(base_url)
#        urls += grab_job_links(soup)
#    except:
#        continue
#    
#def get_posting(url):
#    soup = get_soup(url)
#    title = soup.find(name='h3').getText().lower()
#    posting = soup.find(name='div', attrs={'class': "jobsearch-JobComponent"}).get_text()
#    return title, posting.lower()
#    

