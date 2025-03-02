import pymysql
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()

username = os.getenv("BBDD_USERNAME")
password = os.getenv("BBDD_PASSWORD")
host = os.getenv("BBDD_HOST")
port = 3306

db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
)

cursor = db.cursor()
create_db = '''CREATE DATABASE formula_1'''
cursor.execute(create_db)
cursor.connection.commit()
use_db = ''' USE formula_1'''
cursor.execute(use_db)
create_table = '''
CREATE TABLE interactions (
    id INT NOT NULL auto_increment,
    question TEXT,
    response TEXT,
    session_id  VARCHAR(50)  NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    primary key (id)
)
'''
cursor.execute(create_table)
db.commit()
cursor.close()
db.close()