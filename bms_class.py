# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:28:54 2018

@author: p.soni
"""

import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


class BMSData():
    
    def __init__(self, region):
        
        site = "https://in.bookmyshow.com/" + region + "/movies/"
        
        try:
            page = requests.get(site)
        except:
            raise ConnectionError("Check your Internet Connection")
            
        soup = BeautifulSoup(page.content, "html.parser")
        
        self.body = soup.find("body")
        
        self.get_movie_data()
        
        self.fill_DataFrame()
        
        self.topten = self.topten_movies()
        
        self.nearby_theatre = self. nearby_cinemas()
        
    def removekey(self, d, key):
        r = dict(d)
        del r[key]
        return r
    
    def get_movie_data(self):
        movie_col = self.body.find(class_ = "mv-row")
        
        if movie_col is None :
            raise ValueError("OOPS! No movies near you")
        
        self.movie_cards = movie_col.find_all(class_ = "wow fadeIn movie-card-container")

        self.col_names = list(self.removekey(self.movie_cards[0].attrs,"class").keys())
        
        self.col_names.extend(["event-code", "event-name"])
        
        self.movie_df = pd.DataFrame(columns=self.col_names)
        
    def topten_movies(self):
        top = self.body.find("div", {"class" : "__col-top-ten"})
        top_list = top.find_all(class_ = "movies sa-data-plugin _top10")
        
        top_ten = []
        
        for movie in top_list:
            top_ten.append(self.movie_df[self.movie_df.event_code == movie["data-event-code"]]["event_name"].to_string(index=False))
            
        return top_ten

    def fill_DataFrame(self):
        
        for card in self.movie_cards:
            event = card.find('ul', {"class" : "rating-stars"})
            
            new = self.removekey(card.attrs, "class")
            new["event-code"] = event["event-code"]
            new["event-name"] = event["event-name"]
            
            card_values = list(new.values())
            new_df = pd.DataFrame(card_values, index=self.col_names).T
        
            self.movie_df = pd.concat([self.movie_df, new_df], axis=0)
    
        self.movie_df.reset_index(inplace=True)
        self.movie_df.drop("index", inplace=True, axis=1)
        
        self.movie_df = self.movie_df.rename(index=str, columns={"data-selector": "type", "data-filter" : "data_filter", "data-language-filter" : "languages", "data-dimension-filter" : "format"
                                                       ,"data-search-filter" : "data_search_filter", "data-genre-filter" : "genre", "event-code" :  "event_code", "event-name" :  "event_name"})
        
        self.movie_df.drop(["data_filter", "data_search_filter"], inplace=True, axis=1)
        
        self.movie_df.replace("", np.nan, inplace=True)
        
        self.movie_df.dropna(inplace=True)
        
        self.filters_ = ["language", "genre", "format"]
        
        for filter_ in self.filters_:
            self.filters(filter_)

        self.movie_df.drop(["languages", "genre", "format"], inplace=True, axis=1)
        
    
    def filters(self, filter_):
        filter_values = self.get_filters(filter_)
        
        if(filter_ == "language"):
            self.language_filter_list = filter_values
        
        elif(filter_ == "genre"):  
            self.genre_filter_list = filter_values
               
        elif(filter_ == "format"):  
            self.format_filter_list = filter_values
        
        for filter_col in filter_values:
            self.movie_df[filter_col] = np.nan
        
        for index, row in self.movie_df.iterrows():
            
            if(filter_ == "language"):
                for i in range(1, len(row.languages.split("|"))):
                    self.movie_df.set_value(index, row.languages.split("|")[i], int(1))
            
            elif(filter_ == "genre"):  
                for i in range(1, len(row.genre.split("|"))):
                    self.movie_df.set_value(index, re.sub('[^A-Za-z0-9]+', '', row.genre.split("|")[i].lower()), int(1))
                    
            elif(filter_ == "format"):  
                for i in range(1, len(row.format.split("|"))):
                    self.movie_df.set_value(index, row.format.split("|")[i], int(1))
                    
        
        self.movie_df[filter_values] = self.movie_df[filter_values].fillna(0).astype(int)
        
    def get_filters(self, filter_):
        class_ = filter_ + " __filter-list"
        
        filter_class = self.body.find(class_=class_)
        
        filter_list = filter_class.find_all('input', {"value" : True})
        
        if(filter_ == "genre"):
            filter_values = [filter_value["value"].lower() for filter_value in filter_list]
        else:
            filter_values = [filter_value["value"] for filter_value in filter_list]
        
        return filter_values
    
    def nearby_cinemas(self):
        nearby_sec = self.body.find("div", {"class" : "main-triales-sect" })
        
        nearby_list_text = nearby_sec.find(class_ = "top-cinema column").getText()
        
        nearby_list = list(filter(None, nearby_list_text.split("\n")))
        
        return [str(list(filter(None,nearby_list[i].split(" | ")))[0]) for i in range(1, len(nearby_list))]
        
    @property
    def get_movies(self):
        return list(self.movie_df.event_name)
    
    @property
    def get_filter_list(self):
        return self.filters_
    
    @property
    def get_DataFrame(self):
        return self.movie_df
    
    @property
    def get_format_list(self):
        return self.format_filter_list
    
    @property
    def get_language_list(self):
        return self.language_filter_list
    
    @property
    def get_genre_list(self):
        return self.genre_filter_list
    
    @property
    def get_topten_movies(self):
        return self.topten
    
    @property
    def get_nearby_theatre(self):
        return self.nearby_theatre


bms = BMSData("pune")

#print(bms.movie_df)
