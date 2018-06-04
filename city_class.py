#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 22:15:13 2018

@author: piyush
"""


import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import warnings


class city():
    
    def __init__(self):
        
        warnings.filterwarnings("ignore")
        
        site = "https://in.bookmyshow.com/"
        
        try:
            page = requests.get(site)
        except:
            raise ConnectionError("Check your Internet Connection")
                    
        soup = BeautifulSoup(page.content, "html.parser")
        
        body = soup.find("body")
        
        popular_cities = self.fetch_popular_cities(body)
        other_cities = self.fetch_other_cities(body)
        
        self.city_df = pd.concat([popular_cities, other_cities], join = "inner").reset_index(drop=True)
        
        return
        
    def get_name(self, string):
        """
        Remove any whitespace or newline
        """
        return re.sub(r'\n\s*\n', r'\n\n', string.strip(), flags=re.M)

    def fetch_popular_cities(self, body):
        top_cities = body.find(class_ = "__top-cities")    
        
        region_list = top_cities.find_all(class_ = "region-list")
        
        popular_cities = []
        popular_cities_codes = []
        
        for region in region_list:
            popular_cities.append(self.get_name(region.a.get_text()))
            
            onclick_attr = region.a.attrs['onclick']
            
            city_code = onclick_attr[onclick_attr.find("(")+1 : onclick_attr.find(")")].split(',')[0].strip('\'')
            
            popular_cities_codes.append(city_code)
            
        popular_city_df = pd.DataFrame({"city_name" : popular_cities, "city_id" : popular_cities_codes})
    
        return popular_city_df
#print(popular_cities)
    
    def fetch_other_cities(self, body):
        other_cities_soup = body.find(class_ = "others-cities-list")
        
        other_city_names = other_cities_soup.find_all(class_ = "city-name")
        
        other_cities = []
        other_cities_codes = []
        
        for city_name in other_city_names:
            other_cities.append(self.get_name(city_name.a.get_text()))
            
            onclick_attr = city_name.a.attrs['onclick']
            
            city_code = onclick_attr[onclick_attr.find("(")+1 : onclick_attr.find(")")].split(',')[0].strip('\'')
            
            other_cities_codes.append(city_code)
            
        other_city_df = pd.DataFrame({"city_name" : other_cities, "city_id" : other_cities_codes})

        return other_city_df
    
    @property
    def get_cities(self):
        return self.city_df
    
if __name__ == "__main__" :
    cities = city()
    print(cities.get_cities)