#https://www.dooinauction.com/auction/search/?court1%5B%5D=101%7C102%7C103%7C104%7C105&price2=200000000&km_status=ing&mul_type%5B%5D=121&mul_type%5B%5D=124&mul_type%5B%5D=111&build_area1=38&addr1%5B%5D=%EC%84%9C%EC%9A%B8&current_page=1&records_per_page=30&orderby=low_price&order=asc 
#리스트를 가져오기

import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from typing import List

bucket= "realestate"

client = InfluxDBClient(url="http://localhost:8086", token="uULKZwxtEOUwW7t23lzbmRHkEEACdhmWAfAoyqiPidsMeEm9My1V7hdyO89RSJAoEQcJVcgenmLFUmBfRXFknw==", org="simmy")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


driver = webdriver.Chrome()
driver.get('https://www.dooinauction.com/auction/search/?court1%5B%5D=101%7C102%7C103%7C104%7C105&price2=200000000&km_status=ing&mul_type%5B%5D=121&mul_type%5B%5D=124&mul_type%5B%5D=111&build_area1=38&addr1%5B%5D=%EC%84%9C%EC%9A%B8&current_page=1&records_per_page=30&orderby=low_price&order=asc')
driver.implicitly_wait(1)

table =[]

card_num = driver.find_elements(by=By.CSS_SELECTOR, value='#search-form > div:nth-child(2) > div > div.product-list-inner > div.product-list.auction-product-list > div.product-list-body > div > div')
card_num_1 = len(card_num)

print(card_num)
for card in card_num:
    case_id: str = card.find_element(By.CSS_SELECTOR, 'div.product-card-cell.product-card-address > div > span').text.replace('지도 보기', '')
    house_type: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > div > div').text
    address: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > span').text
    spec: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > div > div:nth-child(1)').text
    senior_tenant: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-address > div > a > div > div.size-txt.color-warm-pink').text
    appraisal: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-price > div > div.label-price-cell.label-appraiser-price > div.price-value').text
    lowest_price: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-price > div > div.label-price-cell.label-lowest-price > div.price-value').text
    decline_time: str = card.find_element(By.CSS_SELECTOR,'div.product-card-cell.product-card-stats > div > div:nth-child(2)').text

    p = Point(bucket)\
        .tag("case_id", case_id)\
        .field("house_type", house_type)\
        .field("address", address)\
        .field("spec", spec)\
        .field("senior_tenant", senior_tenant) \
        .field("appraisal", appraisal) \
		.field("lowest_price", lowest_price) \
        .field("decline_time", decline_time) 
    
    write_api.write(bucket=bucket, org="simmy", record=p)