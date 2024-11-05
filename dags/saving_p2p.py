# 피플 펀드

import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from typing import List
import psycopg2
from psycopg2 import sql


bucket= "p2p"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.peoplefund.co.kr/investing/list?type=all&is_investable=true')
driver.implicitly_wait(1)

table =[]

card_num = driver.find_elements(by=By.CSS_SELECTOR, value='#__next > section > section.phoenix-1yms34e.exy32f317 > div.phoenix-fvpicd.exy32f318')[0].find_elements(By.TAG_NAME, 'a')
card_num_1 = len(card_num)

print("card_num:   ", card_num_1)
for card in card_num:
    information: List[str] = card.text.split('\n')
    table.append([information])


def create_table_to_postgres(host, database, user, password, table_name, data):
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        drop_table_query= """
        DROP TABLE IF EXISTS p2p;
        """
        cursor.execute(drop_table_query)
        print("table droped successfully")

        create_table_if_not_exist_query = """
        CREATE TABLE IF NOT EXISTS p2p (
            id SERIAL PRIMARY KEY,
            information TEXT NOT NULL
        );
        """ 
        cursor.execute(create_table_if_not_exist_query)

        print(f"1 table created successfully.")

        insert_query = sql.SQL(
            'INSERT INTO p2p (information) VALUES (%s)'
        ).format(table=sql.Identifier(table_name))

        cursor.execute(insert_query, data[0])
        connection.commit()

    except Exception as error:
        print(f"Error inserting data: {error}")
        if connection:
            connection.rollback()
    
    finally:
        if connection:
            cursor.close()
            connection.close()

create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', bucket, table)