Acquires unstructured data from BookMyShow clean it and feed it to MySQL server for remote access.  
Scrapped data is structured mainly in 4 data tables:  

<b>CITY_Table</b> : It contains information of all the cities compatible with BookMyShow.  
* <b>Columns</b> : "city_id", "city_name"  

<b>MOVIE_Table</b> : It contains information about movies that are screened on cities supported by BMS all over INDIA.
* <b> Columns</b> : "movie_name", "movie_id", "city_id", 'booking_links', "lang", "format_"   

<b>THEATRE_Table</b> : It contains information(name, latitude, longitude, city) about all the theatres located in INDIA which supports booking through BMS.
* <b> Columns </b> : "theatre_ID", "theatre_name", "theatre_lat", "theatre_long", "city", "city_ID"

<b>SHOW_Table</b> : It contains information of shows i.e. show_timings, show_dates, percentage of seats available, of movies screening in theatres all over INDIA. 
* <b> Columns </b> : "show_ID", "theatre_ID", "movie_ID", "show_date", "show_timing", "seat_percent_available"


## Files:
* <b>bms_scrapper.py</b> :
Extract movies information for a particular region.
  - <b>get_topten_movies</b> : Extracts list of top ten movies screening in particuar region.
  - <b>get_nearby_theatres</b> : Lists names of nearby theatres to you location.

* <b>city_class.py</b> :
Class to extract cities supported by BookMyShow.  
city_table : city_ID, city_name

* <b>movie_class.py</b> :
Class to extract data of movies showing in all cities supported.  
MOVIE table : movie_ID, movie_name, city_ID 

* <b>theatre_show.py</b> :
  - Extracts details about theatre like latitude and longitutde of theatres, city.  
  - Extracts details about shows like show_timings and dates, theatre and city.
  
* <b>sql.py</b> :  
 This script push the collected data to an remote MySQL server.
 
## How to run:
To fetch information about certain region, just run: <b>bms_scrapper.py</b>  

bms = BMSData("ncr")  
print(bms.get_topten_movies)

