from influxdb import InfluxDBClient

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
        self.client =  None #InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

    def insert(self, json_body):
        try:
            self.client.write_points(json_body)
        except:
            return "에러가 발생했습니다."
        return True

    def update(self, query):
        result = self.client.query(query)
        return result

    def delete(self, query):
        result = self.client.query(query)
        return result

    def drop_database(self, name):
        try:
            self.client.drop_database(name)
        except:
            return "에러가 발생했습니다."
        return True