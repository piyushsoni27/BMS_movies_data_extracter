# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 20:30:43 2017

@author: Piyush
"""
import time
#from bms_now_showing import all_movies_name, event_codes, site, movies_names
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver_path = "F:\BMS_movies_data_extracter\chromedriver_win32\chromedriver.exe"
movie = 'Baadshaho'
event_code = 'ET00035720'
region = 'noida'

site = "https://in.bookmyshow.com/" + region + "/movies/" + movie + '/' + event_code + '/user-reviews'

browser = webdriver.Chrome(driver_path)

browser.get(site)

time.sleep(1)

user_review_tab = browser.find_element_by_xpath('//*[@id="user-review"]')

user_review_tab.click()
a=1
while a:
        # Find the first element on the page, so we can scroll down using the
        # element object's send_keys() method
        user_review_tab = browser.find_element_by_xpath('//*[@id="user-review"]')
        user_review_tab.send_keys(Keys.PAGE_DOWN)
        a-=1