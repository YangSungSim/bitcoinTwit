#from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient, Point
import json

# client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
#  client.write_points(json_body)
#
# json_body = [
#         {
#             "measurement": "cpu_load_short",
#             "tags": {
#                 "host": "server01",
#                 "region": "us-west"
#             },
#             "time": "2009-11-10T23:00:00Z",
#             "fields": {
#                 "value": 0.64
#             }
#         }
#     ]

# result = client.query('select value from cpu_load_short;')
# print("Result: {0}".format(result))

class InfluxOrm:

    def __init__(self):
        self.json_body = None
        self.query = None
        self.client = InfluxDBClient(url="http://localhost:8086", token="KPTWhc52uC_awgqmqzjv6wIJkxAg1dCrBU2dBGkCehs2n3kxzwWA7AQDUd701oJX6yvn9ABamUgGtosvhuBejA==", org="simmy") #InfluxDBClient('localhost', 8086, 'admin', '12345678', 'p2p')
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()
        self.org = 'simmy'

    def insert(self, json_body):
        try:
            self.client.write_api(json_body)
        except:
            return "에러가 발생했습니다."
        return True

    def update(self, query):
        result = self.query_api.query(org=self.org, query=query)
        return result

    def delete(self, start, stop, bucket):
        result = self.delete_api.delete(start=start, stop=stop, bucket=bucket, org="simmy")
        return result
    
    def select(self, query):
        result = self.query_api.query(org=self.org, query=query)
        records = [record.values for table in result for record in table.records]
        return str(records)