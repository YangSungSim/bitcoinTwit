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
import psycopg2
from psycopg2 import sql
import yfinance as yf

bucket= "ETF"


df = investpy.get_etfs(country="United States")

etf_table = []
for index, row in df.iterrows():
    try:
        data = pd.DataFrame()
        data['close'] = Symbol(row['symbol']).price_history()[0]['close']
        data['date'] = Symbol(row['symbol']).price_history()[0]['close'].index

        for da in data.values:
            etf_table.append([row['symbol'], float(da[0]), da[1]])

        if index > 50:
            break

    except Exception as e:
        continue

print("etf finished")

us_index_table = []
us_bucket = "US_INDEX"

# today = dt.datetime.now() 
# formatted_today = today.strftime('%Y-%m-%d')
# yesterday = today - timedelta(days=1)
# formatted_yesterday = yesterday.strftime('%Y-%m-%d')

def write_stock_data(symbol, item_tag):
    data = yf.Ticker(symbol).history(period="5d")
    pd.options.display.float_format = '{:.4f}'.format
    data['item'] = item_tag
    data['date'] = data.index
    modified = data[['item','Close','date']]
    us_index_table.append(modified.values.tolist())

# dowjones DJIA
write_stock_data('^DJI', 'DJI')

# NASDAQ
write_stock_data('^IXIC', 'NASDAQ')

# S&P 500
write_stock_data('^GSPC', 'S&P500')

# KOSPI
write_stock_data('^KS11', 'KOSPI')

# S&P based ETF
write_stock_data('VOO', 'VOO')
write_stock_data('SDY', 'SDY')


def create_table_to_postgres(host, database, user, password, table_name, data):
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        drop_table_query= f"""
        DROP TABLE IF EXISTS {table_name};
        """

        cursor.execute(drop_table_query)

        print("1 table droped successfully")

        create_table_if_not_exist_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            item VARCHAR(50) NOT NULL,
            close VARCHAR(50) NOT NULL,
            date VARCHAR(50) NOT NULL
        );
        """ 
        cursor.execute(create_table_if_not_exist_query)

        print(f"1 table created successfully.")

        insert_query = None
        if table_name == 'ETF':
            insert_query = sql.SQL(
                'INSERT INTO ETF (item, close, date) VALUES (%s, %s, %s)'
            ).format(table=sql.Identifier(table_name))
        else:
            insert_query = sql.SQL(
                'INSERT INTO US_INDEX (item, close, date) VALUES (%s, %s, %s)'
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


create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', bucket, etf_table)
create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', us_bucket, us_index_table)