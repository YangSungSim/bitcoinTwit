import psycopg2
from psycopg2 import sql


class PostgresOrm:

    def __init__(self):
        self.query = None
        self.host = 'localhost'
        self.database = 'postgres'
        self.user = 'admin'
        self.password ='postgres'
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def select(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def delete(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def drop(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
