# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests

region = "noida"


def movie_name(movie_n):
    movie = ""
    movie_na = re.split("-", movie_n)
    for i in range(1, len(movie_na)-1):
        movie += movie_na[i] + "-"
        
    movie += movie_na[len(movie_na)-1]
    
    return movie

    
languages = ""
lang_ind = 1

site = "https://in.bookmyshow.com/" + region + "/movies/"

try:
    page = requests.get(site)
except:
    raise ConnectionError("Check your Internet Connection")
    
soup = BeautifulSoup(page.content, "html.parser")

body = soup.find("body")

language_filter_list = body.find(class_="language __filter-list")
language_filters = language_filter_list.find_all('input', {"value" : True})

languages = [language["value"] for language in language_filters]

if(len(languages) != 0): languages.insert(0, 'all')
else: raise SystemExit("No movies in selected region")    

print("Select language of movie (e.g. 2 for " + languages[1] + ") : \n")

for i in range(len(languages)):
    print(i+1, ". " + languages[i])
    
lang_ind = input("Please enter number corresponding to language:\n")

lang = languages[int(lang_ind)-1]

site_filter = "https://in.bookmyshow.com/" + region + "/movies/" + lang

try:
    page_filter = requests.get(site_filter)
except:
    raise ConnectionError("Check your Internet Connection")
    
soup = BeautifulSoup(page_filter.content, "html.parser")

body_filter = soup.find("body")

movie_col = body_filter.find(class_ = "mv-row")

all_movies = movie_col.find_all('div', {"data-selector" : True})
    
events = movie_col.find_all('ul', {"class" : "rating-stars"})

## Mask for only movies in now_showing
mask = [movie["data-language-filter"]!="" for movie in all_movies]

movies = [all_movies[i]["data-search-filter"] for i in range(len(all_movies)) if mask[i]]

## Movie names used for creating link to the movies
all_movies_name = list(map(movie_name, movies))
#print(all_movies_name)

## Actual movies names
movies_names = [events[i]["event-name"] for i in range(len(events)) if mask[i]]

event_codes = [events[i]["event-code"] for i in range(len(events)) if mask[i]]
print(movies_names)
##print(event_codes)