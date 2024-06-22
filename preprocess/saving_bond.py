import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

# 채권 정보 수집 모듈

#한국 국채 회사채
bucket= "korea_bond"

client = InfluxDBClient(url="http://localhost:8086", token="uULKZwxtEOUwW7t23lzbmRHkEEACdhmWAfAoyqiPidsMeEm9My1V7hdyO89RSJAoEQcJVcgenmLFUmBfRXFknw==", org="simmy")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


driver = webdriver.Chrome()
driver.get('https://datacenter.hankyung.com/rates-bonds')
driver.implicitly_wait(1)

table =[]
row_select_list = [2,3,5]
for num in row_select_list:
    path = '#container > div > div.table-stock-wrap > table.table-stock.table-daily > tbody > tr > td:nth-child(' + str(num) + ') > span'
    col_data = driver.find_elements(by=By.CSS_SELECTOR, value=path)
    col_data = list(map(lambda x : str(x.text).strip(), col_data))
    col_data_list = []
    for j in col_data:
        if j != '' and len(j) > 0:
            col_data_list.append(j)
    if (len(col_data_list)) > 0:
        table.append(col_data_list)

submit_button = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/ul/li[2]/a')
submit_button.click()
driver.implicitly_wait(1)

for num in range(4, 7):
    path = '#container > div > div.table-stock-wrap > table.table-stock.type-no-bar.table-period > tbody > tr > td:nth-child(' + str(num) + ') > span'
    col_data = driver.find_elements(by=By.CSS_SELECTOR, value=path)
    col_data = list(map(lambda x : str(x.text).strip(), col_data))
    col_data_list = []
    for j in col_data:
        if j != '' and len(j) > 0:
            col_data_list.append(j)

    if (len(col_data_list)) > 0:
        table.append(col_data_list)

df = pd.DataFrame(table)
df = df.transpose()
df.columns = ['item_name', 'close', 'change', '1month', '6month', '1year']
print(df)



for i in range(0, len(df)):
    row = df.iloc[i,:]
    print("row : ", row)
    p = Point("bond")\
        .tag("date", datetime.datetime.now())\
        .field("kind", row['item_name'])\
        .field("close", row['close'])\
        .field("change", row['change'])\
        .field("1month", row['1month']) \
        .field("6month", row['6month']) \
        .field("1year", row['1year'])
    
    write_api.write(bucket=bucket, org="simmy", record=p)

# 한국 국채 끝
submit_button = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[2]/ul/li[2]/a')
submit_button.click()
driver.implicitly_wait(1)

# 미국 회사채, 국채
bucket= "us_bond"
table =[]
row_select_list = [2,3,5]
for num in row_select_list:
    path = '#container > div > div.table-stock-wrap > table.table-stock.table-daily > tbody > tr > td:nth-child(' + str(num) + ') > span'
    col_data = driver.find_elements(by=By.CSS_SELECTOR, value=path)
    col_data = list(map(lambda x : str(x.text).strip(), col_data))
    col_data_list = []
    for j in col_data:
        if j != '' and len(j) > 0:
            col_data_list.append(j)
    if (len(col_data_list)) > 0:
        table.append(col_data_list)

submit_button = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/ul/li[2]/a')
submit_button.click()
driver.implicitly_wait(1)

for num in range(4, 7):
    path = '#container > div > div.table-stock-wrap > table.table-stock.type-no-bar.table-period > tbody > tr > td:nth-child(' + str(num) + ') > span'
    col_data = driver.find_elements(by=By.CSS_SELECTOR, value=path)
    col_data = list(map(lambda x : str(x.text).strip(), col_data))
    col_data_list = []
    for j in col_data:
        if j != '' and len(j) > 0:
            col_data_list.append(j)

    if (len(col_data_list)) > 0:
        table.append(col_data_list)

df = pd.DataFrame(table)
df = df.transpose()
df.columns = ['item_name', 'close', 'change', '1month', '6month', '1year']
print(df)



for i in range(0, len(df)):
    row = df.iloc[i,:]
    print("row : ", row)
    p = Point("bond")\
        .tag("date", datetime.datetime.now())\
        .field("kind", row['item_name'])\
        .field("close", row['close'])\
        .field("change", row['change'])\
        .field("1month", row['1month']) \
        .field("6month", row['6month']) \
        .field("1year", row['1year'])
    
    write_api.write(bucket=bucket, org="simmy", record=p)