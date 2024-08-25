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
from concurrent.futures import ThreadPoolExecutor

bucket= "etf"

client = InfluxDBClient(url="http://localhost:8086", token="TjaHFUdpuEjk3zmsNFNL0JRnZkVzXpoNPLqTJkmuStQ8XhZU_-3qpSSk1J-MoJ2D6YBXVeeS-sTxvOo3MHYF-w==", org="simmy")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


df = investpy.get_etfs(country="United States")
df_top_snp = df[df['name'].str.contains("S&P", case=False, na=False)]

def fetch_and_write_data(row):
    try:
        symbol = row['symbol']
        # price_history를 한 번만 호출
        history = Symbol(symbol).price_history()[0]
        data = pd.DataFrame({
            'close': history['close'],
            'date': history['close'].index
        })

        points = []
        for _, da in data.iterrows():
            p = Point(bucket)\
                .tag("item", symbol)\
                .field("close", float(da['close']))\
                .time(da['date'].strftime('%Y-%m-%d %H:%M:%S'))
            points.append(p)

        # 한 번에 데이터를 InfluxDB에 씁니다.
        if points:
            write_api.write(bucket=bucket, org="simmy", record=points)
    except Exception as e:
        print(f"Error processing {row['symbol']}: {e}")

# 멀티스레딩을 사용하여 병렬 처리
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(fetch_and_write_data, [row for _, row in df_top_snp.iterrows()])


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