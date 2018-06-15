#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:34:51 2018

@author: piyush
"""

from sqlalchemy import create_engine
import pandas as pd

host = "0.0.0.0"
user = "root"
passwd = "qwerty1234"
db = "bmsdb"

engine = create_engine("mysql+mysqldb://root:qwerty1234@127.0.0.1/bmsdb")

#con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

city_table = pd.read_csv("CITY_Table.csv")
movie_table = pd.read_csv("MOVIE_Table.csv")
theatre_table = pd.read_csv("THEATRE_Table.csv")
show_table = pd.read_csv("SHOW_Table.csv")

city_table.to_sql(con=engine, name='CITY_Table', if_exists='replace')
movie_table.to_sql(con=engine, name='MOVIE_Table', if_exists='replace')
theatre_table.to_sql(con=engine, name='THEATRE_Table', if_exists='replace')
show_table.to_sql(con=engine, name='SHOW_Table', if_exists='replace')
