#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:56:33 2018

@author: piyush
"""

import bms_scrapper as bms
import pandas as pd


city_table = pd.read_csv("CITY_Table.csv")
movie_table = pd.DataFrame(columns=["movie_name", "movie_id", "city_id"])

for i in range(len(city_table)):
    print(i)
    region = city_table.city_name.iloc[i]
    
    try:
        BMS_region = bms.BMSData(region)
    except:
        continue
    
    movies_info = BMS_region.get_movies_info.rename(index=str, columns={"event_name" : "movie_name", "event_code" : "movie_id"})
   # movie_table_region = 
    movies_info["city_id"] = city_table.city_id.iloc[i]
    movie_table = pd.concat([movie_table, movies_info[["movie_name", "movie_id", "city_id"]]])
    #print(region)
    #print(BMS_region.get_movies_info)

movie_table.reset_index(inplace=True)
movie_table.to_csv("MOVIE_Table.csv", index = False, header = True)