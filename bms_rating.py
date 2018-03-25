# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:30:19 2017

@author: Piyush
"""
from bms_now_showing import all_movies_name, event_codes, site, movies_names
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


hearts_dict = {}
critics_rating_dict = {}
users_rating_dict = {}

def get_heart_rating_BMS(body):
    heart_rating_class = body.find("div", {"class" : "heart-rating"})
    heart_rating = heart_rating_class.find('span', {'class' : '__percentage'}).text
    return heart_rating

def get_critics_rating_BMS(body):
    critics_rating_class = body.find("div", {"class" : "critic-rating"})
    critics_rating = critics_rating_class.find("ul", {"class" : "rating-stars"})["data-value"]
    return critics_rating

def get_user_rating_BMS(body):
    user_rating_class = body.find("div", {"class" : "user-rating"})
    user_rating = user_rating_class.find("ul", {"class" : "rating-stars"})["data-value"]
    return user_rating

def data_rating(movie, event_code, actual_movie_name):
    site_movie = site + movie + "/" + event_code + "/"
    
    page_movie = requests.get(site_movie)
    
    soup_movie = BeautifulSoup(page_movie.content, "html.parser")
    
    body_movie = soup_movie.find("body")
    
    try:
        hearts = get_heart_rating_BMS(body_movie)
       ## print(hearts)
    except: hearts = np.nan
    
    try:
        critics_rating = get_critics_rating_BMS(body_movie)
        ## print(critics_rating)
    except: critics_rating = np.nan
    
    try:
        user_rating = get_user_rating_BMS(body_movie)
        ## print(user_rating)
    except: user_rating = np.nan
    
    hearts_dict[actual_movie_name] = hearts
    critics_rating_dict[actual_movie_name] = critics_rating
    users_rating_dict[actual_movie_name] = user_rating

    return

for i in range(len(event_codes)):
    data_rating(all_movies_name[i], event_codes[i], movies_names[i])

ratings = pd.DataFrame([hearts_dict, critics_rating_dict, users_rating_dict]).T
ratings.columns = ["Hearts", "Critics_Ratings", "User_Ratings"]

print(ratings)

    