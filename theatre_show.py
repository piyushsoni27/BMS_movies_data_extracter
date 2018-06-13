# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:34:21 2018

@author: p.soni
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

site = "https://in.bookmyshow.com/buytickets/veere-di-wedding-national-capital-region-ncr/movie-ncr-ET00042975-MT/20180614"

try:
    print("Extracting Data, please wait...\n")
    page = requests.get(site)
except:
    raise ConnectionError("Check your Internet Connection")
    
soup = BeautifulSoup(page.content, "html.parser")

body = soup.find("body")

showtimes = soup.find("section", {"class" : ["phpShowtimes", "showtimes"]})

venues = showtimes.find_all("li", class_ = "list")

theatre_cols = ["theatre_ID", "theatre_name", "theatre_lat", "theatre_long", "city", "city_ID"]
show_cols = ["show_ID", "theatre_ID", "movie_ID", "show_date", "show_timing", "seat_percent_available"]

theatre_table = pd.DataFrame(columns = theatre_cols)
show_table = pd.DataFrame(columns = show_cols)

for venue in venues:
    theatre_table = theatre_table.append({"theatre_ID" : venue["data-id"], "theatre_name" : venue["data-name"], "theatre_lat" : venue["data-lat"], "theatre_long" : venue["data-lng"], "city" : venue["data-sub-region-name"], "city_ID" : venue["data-sub-region-id"]}, ignore_index = True)
    
    show_body = venue.find("div", class_ = "body ")
    shows = show_body.find_all("div", {"data-online" : "Y"})
    
    for show_div in shows:
        show = show_div.find("a")
        show_table = show_table.append({"show_ID" : show["data-session-id"], "theatre_ID" : show["data-venue-code"], "movie_ID" : show["data-event-id"], "show_date" : show["data-cut-off-date-time"], "show_timing" : show["data-showtime-code"], "seat_percent_available" : show["data-seats-percent"]}, ignore_index = True)
    
print(theatre_table)
print(show_table )