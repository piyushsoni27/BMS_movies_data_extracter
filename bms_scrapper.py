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
import warnings


class BMSData():
    
    def __init__(self, region):
        
        warnings.filterwarnings("ignore")
        
        site = "https://in.bookmyshow.com/" + region + "/movies/"
        
        try:
            print("Extracting Data, please wait...\n")
            page = requests.get(site)
        except:
            raise ConnectionError("Check your Internet Connection")
            
        soup = BeautifulSoup(page.content, "html.parser")
        
        self.isEmpty = False 
        
        self.body = soup.find("body")
        
        self.fetch_movie_data()
        
        if(self.isEmpty):
            columns = ['event_name', 'event_code', 'format', 'genre', 'languages', 'type', 'booking_links']
            self.master_df = pd.DataFrame(columns=columns)
            return
        
        self.fill_DataFrame()
        
        self.topten = pd.Series(self.fetch_topten_movies())
        
        self.nearby_theatre = pd.Series(self.fetch_nearby_cinemahalls())
        
        return
               
    def removekey(self, d, key):
        r = dict(d)
        del r[key]
        return r
    
    def fetch_movie_data(self):
        
        movie_col = self.body.find(class_ = "mv-row")
        
        if movie_col is None :
            #raise ValueError("OOPS! No movies near you")
            print("OOPS! No movies near you")
            
            self.isEmpty= True
            return
        
        self.movie_cards = movie_col.find_all(class_ = "wow fadeIn movie-card-container")

        self.col_names = list(self.removekey(self.movie_cards[0].attrs,"class").keys())
        
        self.col_names.extend(["event-code", "event-name"])
        
        self.master_df = pd.DataFrame(columns=self.col_names)
        
        return
        
    def fetch_topten_movies(self):
        top = self.body.find("div", {"class" : "__col-top-ten"})
        top_list = top.find_all(class_ = "movies sa-data-plugin _top10")
        
        top_ten = []
        
        for movie in top_list:
            top_ten.append(self.master_df[self.master_df.event_code == movie["data-event-code"]]["event_name"].to_string(index=False))
            
        return top_ten

    def fill_DataFrame(self):
        
        for card in self.movie_cards:
            
            event = card.find('ul', {"class" : "rating-stars"})
            
            new = self.removekey(card.attrs, "class")
            new["event-code"] = event["event-code"]
            new["event-name"] = event["event-name"]
            
            card_values = list(new.values())
            new_df = pd.DataFrame(card_values, index=self.col_names).T
            
            new_df = self.fetch_booking_links_with_language_and_format(card, event["event-name"], new_df)
            #new_df["booking_links"] = book_link 

            self.master_df = pd.concat([self.master_df, new_df], axis=0)

    
        self.master_df.reset_index(inplace=True)
        self.master_df.drop("index", inplace=True, axis=1)
        
        self.master_df = self.master_df.rename(index=str, columns={"data-selector": "type", "data-filter" : "data_filter", "data-language-filter" : "languages", "data-dimension-filter" : "format"
                                                       ,"data-search-filter" : "data_search_filter", "data-genre-filter" : "genre", "event-code" :  "event_code", "event-name" :  "event_name"})
        
        self.master_df.drop(["data_filter", "data_search_filter"], inplace=True, axis=1)
        
        self.master_df.replace("", np.nan, inplace=True)
        
        #self.master_df.dropna(inplace=True)
        
        self.filters_ = ["language", "genre", "format"]
        
        for filter_ in self.filters_:
            self.create_filters_df(filter_)

       # self.master_df.drop(["languages", "genre", "format"], inplace=True, axis=1)
        self.master_df.dropna(subset=["genre"], inplace=True)
        
        self.master_df.reset_index(drop=True, inplace=True)
        
        columns = ['event_name', 'event_code', 'format', 'genre', 'languages', 'type', 'booking_links']
        
        self.master_df = self.master_df[columns]
        
        return
    
    def create_filters_df(self, filter_):
        """
        Creates DataFarame for language, genre, format filters movie wise
        """
        filter_values = self.fetch_filters(filter_)
        
        if(filter_ == "language"):
            self.language_filter_list = filter_values
            self.language_filter_df = pd.DataFrame(columns=filter_values)
                    
        elif(filter_ == "genre"):  
            self.genre_filter_list = filter_values
            self.genre_filter_df = pd.DataFrame(columns=filter_values)
            
        elif(filter_ == "format"):  
            self.format_filter_list = filter_values
            self.format_filter_df = pd.DataFrame(columns=filter_values)
            

        for index, row in self.master_df.iterrows():
            
            filter_empty_series = pd.DataFrame(np.nan, index=[0], columns=filter_values)
            
            if(filter_ == "language"):

                if(pd.notnull(row.languages)):
                    for i in range(1, len(row.languages.split("|"))):                    
                        filter_empty_series[row.languages.split("|")[i]] = 1 
                    
                self.language_filter_df = pd.concat([self.language_filter_df, filter_empty_series], ignore_index=True)
            
            elif(filter_ == "genre"):  
                if(pd.notnull(row.genre)):
                    for i in range(1, len(row.genre.split("|"))):
                        filter_empty_series[re.sub('[^A-Za-z0-9]+', '', row.genre.split("|")[i].lower())] = 1 
                    
                self.genre_filter_df = pd.concat([self.genre_filter_df, filter_empty_series], ignore_index=True)
            
            elif(filter_ == "format"):  
                if(pd.notnull(row.format)):
                    for i in range(1, len(row.format.split("|"))):
                        filter_empty_series[row.format.split("|")[i]] = 1 
                
                self.format_filter_df = pd.concat([self.format_filter_df, filter_empty_series], ignore_index=True)
            
        
        if(filter_ == "language"):
            self.language_filter_df.fillna(0, inplace=True)
            self.language_filter_df = pd.concat([self.master_df[["event_code", "event_name"]], self.language_filter_df], axis=1)
            
        elif(filter_ == "genre"):  
            self.genre_filter_df.fillna(0, inplace=True)
            self.genre_filter_df = pd.concat([self.master_df[["event_code", "event_name"]], self.genre_filter_df], axis=1)
            
        elif(filter_ == "format"):  
            self.format_filter_df.fillna(0, inplace=True)
            self.format_filter_df = pd.concat([self.master_df[["event_code", "event_name"]], self.format_filter_df], axis=1)
        
        return
    
    def fetch_filters(self, filter_):
        """
        Returns a list of available filters on BMS
        """
        class_ = filter_ + " __filter-list"
        
        filter_class = self.body.find(class_=class_)
        
        filter_list = filter_class.find_all('input', {"value" : True})
        
        if(filter_ == "genre"):
            filter_values = [filter_value["value"].lower() for filter_value in filter_list]
        else:
            filter_values = [filter_value["value"] for filter_value in filter_list]
        
        return filter_values
    
    def fetch_nearby_cinemahalls(self):
        nearby_sec = self.body.find("div", {"class" : "main-triales-sect" })
        
        nearby_list_text = nearby_sec.find(class_ = "top-cinema column").getText()
        
        nearby_list = list(filter(None, nearby_list_text.split("\n")))
        
        return [str(list(filter(None,nearby_list[i].split(" | ")))[0]) for i in range(1, len(nearby_list))]
    
    def fetch_booking_links_with_language_and_format(self, card, s, df):
        experience_holder = card.find(class_ = "experience-holder")
        
        language_based_formats = experience_holder.find_all(class_ = "language-based-formats")
        
        #print(language_based_formats)
        print(s)
        for language_based_format in language_based_formats:
            
            print(language_based_format.find(class_="header").text)
            formats = language_based_format.find_all('span', {"class" : "__format"})
            
            for format_ in formats:
                print(format_.text)

        #if(len(language_based_formats) != 0): print(language_based_formats[0].find('span', {"class" : "__format"}).text)
        
        if(experience_holder.find("a", href=True) is not None):
            df["booking_links"] = "https://in.bookmyshow.com" + experience_holder.find("a", href=True)["href"]
    
        else:
            df["booking_links"] = np.nan
            
        return df
    
    @property
    def get_movies(self):
        return pd.Series(self.master_df.event_name)
    
    @property
    def get_filter_list(self):
        return self.filters_
    
    @property
    def get_movies_info(self):
        return self.master_df
    
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
    def get_nearby_theatres(self):
        return self.nearby_theatre


if __name__ == "__main__":
    bms = BMSData("noida")
    print(bms.get_movies_info)
