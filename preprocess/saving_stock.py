# 미국(INDEX(investpy), ETF(investpy), 배당주(investpy), 한국 kospi, kosdaq.
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import datetime as dt
from datetime import timedelta
from typing import List
import investpy
from tessa import Symbol, SymbolCollection, search
import FinanceDataReader as fdr

bucket= "etf"

client = InfluxDBClient(url="http://localhost:8086", token="uULKZwxtEOUwW7t23lzbmRHkEEACdhmWAfAoyqiPidsMeEm9My1V7hdyO89RSJAoEQcJVcgenmLFUmBfRXFknw==", org="simmy")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


df = investpy.get_etfs(country="United States")

for index, row in df.iterrows():
    try:
        data = pd.DataFrame()
        data['close'] = Symbol(row['symbol']).price_history()[0]['close']
        data['date'] = Symbol(row['symbol']).price_history()[0]['close'].index

        for da in data.values:
            p = Point(bucket)\
            .tag("item", row['symbol'])\
            .field("close", float(da[0]))\
            .field("date", da[1])

            write_api.write(bucket=bucket, org="simmy", record=p)
    except IndexError as e:
        continue


bucket = "us_index"


today = dt.datetime.now() 
formatted_today = today.strftime('%Y-%m-%d')
yesterday = today - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')

def write_stock_data(symbol, item_tag):
    data = fdr.DataReader(symbol, formatted_yesterday, formatted_today)
    for index, row in data.iterrows():
        p = Point(bucket)\
            .tag("item", item_tag)\
            .field("close", row['Close'])\
            .field("date", row['Date'])
        write_api.write(bucket=bucket, org="simmy", record=p)

# dowjones DJIA
write_stock_data('DJI', 'DJI')

# NASDAQ
write_stock_data('IXIC', 'NASDAQ')

# S&P 500
write_stock_data('US500', 'US500')

# KOSPI
write_stock_data('kospi', 'KOSPI')

# KODEX
write_stock_data('KQ11', 'KODEX')

# S&P based ETF
write_stock_data('VOO', 'VOO')
write_stock_data('SDY', 'SDY')