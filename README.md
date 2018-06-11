Scrap movie data and ratings from BookMyShow.

## Files:
### bms_scrapper.py :
Extract movies information for a particular region.

### city_class.py :
Class to extract cities supported by BookMyShow.
city_table : city_ID, city_name

### movie_class.py :
Class to extract data of movies showing in all cities supported.
MOVIE table : movie_ID, movie_name, city_ID 

## How to run:
Please run bms_scrapper.py

bms = BMSData("ncr")
