# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 09:43:27 2019

@author: admin
"""
from datetime import datetime, time, timedelta
import pandas as pd  



def mapping(df_base,df_target,value_to_map,unique_column):
    dict = {}
#    df_base = eval(df_base)    
    df_base = df_base.reset_index(drop = True)      
#    df_target = eval(df_target)         
    count = 0
    for col_value in df_base[unique_column]:
        dict[col_value] = df_base.loc[count,value_to_map]
        count += 1    
    del(count)   
    df_target.loc[:,value_to_map] = df_target.loc[:,unique_column].map(dict)   
    return( df_target )

def more_than_one_mapping (df_base,df_target,values_to_map,unique_column):
        
    for value_to_map in values_to_map:
        df_target = mapping(df_base,df_target,value_to_map,unique_column)

    return( df_target )


def cleaning_data(df):    
    df['value'] = df['value'].replace('\$','',regex=True).replace(',','',regex=True).apply(float)
    df['time_left'] = df['time_left'].replace(' left','',regex=True).replace('d','*86400',regex=True).replace('h','*3600',regex=True).replace('m','*60',regex=True).replace('s','',regex=True).replace(' ','+',regex=True)
    df['seconds_left'] = df['time_left'].apply(eval)
    df['time_left'] = df['seconds_left'].apply(lambda x : str(timedelta(seconds = x)))
    df['shipping'] = df['shipping'].replace('Free Shipping','0').replace('shipping','',regex=True).replace('\+\$','',regex=True).replace(',','',regex=True).replace('N/A','999',regex=True)
    df['shipping'] = df['shipping'].apply(float)
    df['num_bids'] = df['num_bids'].replace('bids','',regex=True).replace('bid','',regex=True).apply(int)       
    return(df)
  
    
def fix_logs_in_files(file1):
    
    try:
  
        a11 = file1.loc[ file1['seconds_left']=='N/D' ,:]
        a12 = file1.loc[ file1['seconds_left']!='N/D' ,:]    
           
        # Mapping
        unique_column = 'link'
        value_to_map = 'auction_end_day'
        df_base = a12[:]
        df_target = a11[:]
        values_to_map = ['auction_end_day','auction_end_hour']
        
        
        df_target = more_than_one_mapping (df_base,df_target,values_to_map,unique_column)
            
        df_target = cleaning_data(df_target)
        
        
        df_base.loc[:,'log'] = df_base.loc[:,'log'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') )
        df_base.loc[:,'seconds_left'] = pd.to_timedelta( df_base.loc[:,'seconds_left'] + ' seconds' )
        
        df_base.loc[:,'ending_time'] = df_base.loc[:,'log'] + df_base.loc[:,'seconds_left']
        
        value_to_map='ending_time'
        
        df_target = mapping(df_base,df_target,value_to_map,unique_column)
        
        
        df_target.loc[:,'real_time_left'] = pd.to_timedelta( df_target.loc[:,'seconds_left'].apply(str) + ' seconds' )
        df_target.loc[:,'log'] = df_target.loc[:,'ending_time'] + df_target.loc[:,'real_time_left']
        
        
        b1 = pd.concat([df_base,df_target])

        return(b1)
        
    except:
        
        file1.loc[:,'log'] = file1.loc[:,'log'].apply(str).apply(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') )
        file1.loc[:,'seconds_left'] = pd.to_timedelta( file1.loc[:,'seconds_left'].apply(str) + ' seconds' )
        
        file1.loc[:,'ending_time'] = file1.loc[:,'log'] + file1.loc[:,'seconds_left']        
        
        
        return(file1)

#####################################################################################################################3
#####################################################################################################################3
#####################################################################################################################3
#####################################################################################################################3
#####################################################################################################################3

    
a1 = pd.read_csv('Auctions_Ebay_MacbookAir1.csv',index_col=0)
a2 = pd.read_csv('Auctions_Ebay_MacbookAir2.csv',index_col=0)
a3 = pd.read_csv('Auctions_Ebay_MacbookAir3.csv',index_col=0)
a4 = pd.read_csv('Auctions_Ebay_MacbookAir4.csv',index_col=0)



b1 = fix_logs_in_files(a1)
b2 = fix_logs_in_files(a2)
b3 = fix_logs_in_files(a3)
b4 = fix_logs_in_files(a4)


AAA = pd.concat([b1,b2,b3,b4])

AAA['value'] = AAA['value'].replace('\$','',regex=True).replace(',','',regex=True).apply(float)

temp = AAA.loc[:,('link','ending_time','value')].sort_values(['link','value'],ascending=False).drop_duplicates('link')


BBB = mapping(df_base=temp,df_target=AAA,value_to_map='ending_time',unique_column='link')



















