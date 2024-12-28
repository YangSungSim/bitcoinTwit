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
    
    def insert(self, table, columns_list, data):
        """
        Inserts data into a given table.
        :param table: Name of the table to insert into
        :param data: duplicate array list
        """
        columns = columns_list
        values = data
        print("data:   ", str(data))
        
        # Prepare the insert query template
        insert_query = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
        ).format(
            table=sql.Identifier(table),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))  # Placeholders for each column
        )

        # Execute the insert query using executemany
        self.cursor.executemany(insert_query, values)
        self.connection.commit()

    def delete(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def drop(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
