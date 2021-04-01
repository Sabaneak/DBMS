import pymysql
from decouple import config

db = pymysql.connect(host="localhost",
                     user="root",
                     password=config('DB_PASS'),
                     database="pms")
