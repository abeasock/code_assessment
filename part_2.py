# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 22:07:55 2017

@author: abeasock
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:12:22 2017

@author: abeasock
"""

import pandas as pd
import requests
import json
import datetime
import time

apikey = '867683adec7c448e9d6171946171107'

df = pd.read_csv('C:/Users/abeasock/Documents/Data/locations.csv')

df['utc_timestamp'] = pd.to_datetime(df['timestamp'])

startTime = time.time()

def get_historical_weather(df):
    
    df_out = pd.DataFrame()
    
    for index, row in df.iterrows():
        try:
            utc_timestamp   = row['utc_timestamp']
            latitude        = row['latitude']
            longitude       = row['longitude']
            date_yyyymmdd   = datetime.datetime.strptime(str(utc_timestamp), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
            utc_hour        = datetime.datetime.strptime(str(utc_timestamp), '%Y-%m-%d %H:%M:%S').strftime("%H").lstrip('0')+'00'
            
            weather_url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' +str(apikey)  + '&q=' + str(latitude) + ',' + str(longitude) + '&format=json&extra=utcDateTime&date=' + date_yyyymmdd  + '&includelocation=yes&tp=1'  
            weather_req = requests.get(weather_url)   
            if weather_req.status_code==200:
                jsondata = json.loads(weather_req.content)
            else:
                print '[ ERROR ] worldweatheronline.com Status Code: ' + str(weather_req.status_code)
            
            record      = [hour_obs for hour_obs in jsondata['data']['weather'][0]['hourly'] if hour_obs['time'] == utc_hour ]
            
            row['nearest_area']      = jsondata['data']['nearest_area'][0]['areaName'][0]['value']
            row['population']        = jsondata['data']['nearest_area'][0]['population']
            row['tempF']             = record[0]['tempF']
            row['weatherDesc']       = record[0]['weatherDesc'][0]['value']
            row['precipMM']          = record[0]['precipMM']
            row['cloudcover']        = record[0]['cloudcover']
        except: 
            print row
            
        df_out = df_out.append(row)
        
    return df_out

df2 = get_historical_weather(df)

endTime = time.time()

elapsedTime = endTime - startTime
print elapsedTime

df2.to_csv('locations_weather.csv', index=False)


