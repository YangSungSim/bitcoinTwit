from kafka import KafkaConsumer
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# bucket = "bitcoin"
# org = "my-org"
# token = "my-token"
# url = "http://localhost:8086"

bucket= "bitcoin"

client = InfluxDBClient(url="http://localhost:8086", token="uULKZwxtEOUwW7t23lzbmRHkEEACdhmWAfAoyqiPidsMeEm9My1V7hdyO89RSJAoEQcJVcgenmLFUmBfRXFknw==", org="simmy")
#client = InfluxDBClient.from_config_file("config.ini")

# 데이터를 쓸 버킷 선택
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

consumer = KafkaConsumer('data-stream',
bootstrap_servers=['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('ascii')))

'''
database: bitcoin
table: realtime_price
column(primary key): kind 
column1: price
column2: input_dt
'''

for message in consumer:
    print("message", message)

    # save realtime data to influx db
    # 데이터 포인트 생성 및 쓰기
    p = Point("realtime_price").tag("kind", message.value['symbol'])\
        .field("price", message.value['price'])\
        .field("input_dt", message.value['timestamp'])
    write_api.write(bucket=bucket, org="simmy", record=p)
