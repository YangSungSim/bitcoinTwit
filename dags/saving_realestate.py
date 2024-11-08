#https://www.dooinauction.com/auction/search/?court1%5B%5D=101%7C102%7C103%7C104%7C105&price2=200000000&km_status=ing&mul_type%5B%5D=121&mul_type%5B%5D=124&mul_type%5B%5D=111&build_area1=38&addr1%5B%5D=%EC%84%9C%EC%9A%B8&current_page=1&records_per_page=30&orderby=low_price&order=asc 
#리스트를 가져오기

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import psycopg2
from psycopg2 import sql
import time

bucket= "realestate"


driver = webdriver.Chrome()
driver.get('https://www.dooinauction.com/auction/search/?court1%5B%5D=101%7C102%7C103%7C104%7C105&price2=200000000&km_status=ing&mul_type%5B%5D=121&mul_type%5B%5D=124&mul_type%5B%5D=111&build_area1=38&addr1%5B%5D=%EC%84%9C%EC%9A%B8&current_page=1&records_per_page=30&orderby=low_price&order=asc')
driver.implicitly_wait(10)
time.sleep(7)

table =[]

card_num = driver.find_elements(by=By.CSS_SELECTOR, value='#search-form > div:nth-child(2) > div > div.product-list-inner > div.product-list.auction-product-list > div.product-list-body > div > div')
card_num_1 = len(card_num)

print(card_num)
for card in card_num:
    try:
        case_id: str = card.find_element(By.CSS_SELECTOR, 'div.product-card-cell.product-card-address > div > span').text.replace('지도 보기', '')
    except Exception as e:
        case_id = 'Null'
    try:
        house_type: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > div > div').text
    except Exception as e:
        house_type: str = 'Null'
    try:
        address: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > span').text
    except Exception as e:
        address: str = 'Null'
    try:
        spec: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > div > div:nth-child(1)').text
    except Exception as e:
        spec: str = 'Null'
    try:
        senior_tenant: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > div > div.size-txt.color-warm-pink').text
    except Exception as e:
        senior_tenant = 'Null'
    try:
        appraisal: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-price > div > div.label-price-cell.label-appraiser-price > div.price-value').text
    except Exception as e:
        appraisal: str = 'Null'
    try:
        lowest_price: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-price > div > div.label-price-cell.label-lowest-price > div.price-value').text
    except Exception as e:
        lowest_price: str = 'Null'
    try:
        decline_time: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-stats > div > div:nth-child(2)').text
    except Exception as e:
        decline_time: str = 'Null'
    
    table.append([case_id, house_type, address, spec, senior_tenant, appraisal, lowest_price, decline_time])

time.sleep(5)

def create_table_to_postgres(host, database, user, password, table_name, data):
    try:
        connection = psycopg2.connect(host=host,database=database,user=user,password=password)
        cursor = connection.cursor()

        drop_table_query= """DROP TABLE IF EXISTS realestate;"""
        cursor.execute(drop_table_query)
        print("table droped successfully")

        create_table_if_not_exist_query = """
        CREATE TABLE IF NOT EXISTS realestate (
            id SERIAL PRIMARY KEY,
            case_id TEXT NOT NULL,
            house_type TEXT NOT NULL,
            address TEXT NOT NULL,
            spec TEXT NOT NULL,
            senior_tenant TEXT NOT NULL,
            appraisal TEXT NOT NULL,
            lowest_price TEXT NOT NULL,
            decline_time TEXT NOT NULL
        );
        """ 
        cursor.execute(create_table_if_not_exist_query)

        print(f"1 table created successfully.")

        print("data:   ", data)
        insert_query = sql.SQL(
            'INSERT INTO realestate (case_id, house_type, address, spec, senior_tenant, appraisal, lowest_price, decline_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        ).format(table=sql.Identifier(table_name))

        cursor.executemany(insert_query, data)
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