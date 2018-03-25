# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:30:19 2017

@author: ANSHUL
"""
from bms_now_showing import all_movies_name, event_codes, site, movies_names
import requests
from bs4 import BeautifulSoup

## movie = all_movies_name[0]
## event_code = event_codes[0]

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

def data_rating(movie, event_code):
    site_movie = site + movie + "/" + event_code + "/"
    
    page_movie = requests.get(site_movie)
    
    soup_movie = BeautifulSoup(page_movie.content, "html.parser")
    
    body_movie = soup_movie.find("body")
    
    try:
        hearts = get_heart_rating_BMS(body_movie)
       ## print(hearts)
    except: hearts = None
    
    try:
        critics_rating = get_critics_rating_BMS(body_movie)
        ## print(critics_rating)
    except: critics_rating = None
    
    try:
        user_rating = get_user_rating_BMS(body_movie)
        ## print(user_rating)
    except: user_rating = None
    
    return (hearts, critics_rating, user_rating)

data = [data_rating(all_movies_name[i], event_codes[i]) for i in range(len(event_codes))]

print(list(zip(movies_names,data)))
    