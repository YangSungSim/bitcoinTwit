import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import psycopg2
import sqlalchemy as sa
from psycopg2 import sql

# 채권 정보 수집 모듈

#한국 국채 회사채
bucket_korea= "korea_bond"

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
        DROP TABLE IF EXISTS korea_bond;
        """
        cursor.execute(drop_table_query)
        drop_table_query2= """
        DROP TABLE IF EXISTS us_bond;
        """
        cursor.execute(drop_table_query2)
        print("table droped successfully")

        create_table_if_not_exist_query = """
        CREATE TABLE IF NOT EXISTS korea_bond (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            close DECIMAL(20, 6) NOT NULL,
            change VARCHAR(255) NOT NULL,
            one_month VARCHAR(255) NOT NULL,
            six_month VARCHAR(255) NOT NULL,
            one_year VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(create_table_if_not_exist_query)

        create_us_bond_table_if_not_exist_query = """
        CREATE TABLE IF NOT EXISTS us_bond (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            close DECIMAL(20, 6) NOT NULL,
            change VARCHAR(255) NOT NULL,
            one_month VARCHAR(255) NOT NULL,
            six_month VARCHAR(255) NOT NULL,
            one_year VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(create_us_bond_table_if_not_exist_query)

        print(f"2 table created successfully.")

        insert_query = sql.SQL(
            'INSERT INTO {table} (item_name, close, change, one_month, six_month, one_year) VALUES (%s, %s, %s, %s, %s, %s)'
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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
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

df_korea_bond = pd.DataFrame(table)
df_korea_bond = df_korea_bond.transpose()
df_korea_bond.columns = ['item_name', 'close', 'change', 'one_month', 'six_month', 'one_year']
print(df_korea_bond)


# 한국 국채 끝
submit_button = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[2]/ul/li[2]/a')
submit_button.click()
driver.implicitly_wait(1)
tab_button = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[3]/ul/li[1]/a')
tab_button.click()
driver.implicitly_wait(5)

# 미국 회사채, 국채
bucket_us= "us_bond"
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
driver.implicitly_wait(5)

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

df_us_bond = pd.DataFrame(table)
df_us_bond = df_us_bond.transpose()
df_us_bond.columns = ['item_name', 'close', 'change', 'one_month', 'six_month', 'one_year']
print(df_us_bond)

create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', bucket_us, df_us_bond.values.tolist())
create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', bucket_korea, df_korea_bond.values.tolist())