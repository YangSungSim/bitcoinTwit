# 피플 펀드

import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from typing import List


bucket= "p2p"

client = InfluxDBClient(url="http://localhost:8086", token="uULKZwxtEOUwW7t23lzbmRHkEEACdhmWAfAoyqiPidsMeEm9My1V7hdyO89RSJAoEQcJVcgenmLFUmBfRXFknw==", org="simmy")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


driver = webdriver.Chrome()
driver.get('https://www.peoplefund.co.kr/investing/list?type=all&is_investable=true')
driver.implicitly_wait(1)

table =[]

card_num = driver.find_elements(by=By.CSS_SELECTOR, value='#__next > section > section.phoenix-197eiju.e3k82g718 > div > a')
card_num_1 = len(card_num)

print(card_num)
for card in card_num:
    information: List[str] = card.text.split('\n')
    category: str = information[0]
    open_yn: str = information[1]
    address: str = information[2]
    year_yield: float = float(information[information.index('연 수익률')+1].replace('%',''))
    period: str = information[information.index('투자 기간')+1]
    collected_money: str = information[-2]
    total_money: str = information[-1]

    p = Point(bucket)\
        .tag("category", category)\
        .field("open_yn", open_yn)\
        .field("address", address)\
        .field("year_yield", year_yield)\
        .field("period", period) \
        .field("collected_money", collected_money) \
		.field("total_money", total_money) 
    
    write_api.write(bucket=bucket, org="simmy", record=p)