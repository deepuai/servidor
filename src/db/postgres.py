import psycopg2

class DatabaseClient:
    __connection = {
        'host': '127.0.0.1',
        'port': '5432',
        'user': 'deepuai',
        'password': 'deepuai'
    }
    __database = None

    @staticmethod
    def initialize(db_name):
        DatabaseClient.__database = psycopg2.connect(
            host = DatabaseClient.__connection['host'],
            port = DatabaseClient.__connection['port'],
            database = db_name,
            user = DatabaseClient.__connection['user'],
            password = DatabaseClient.__connection['password']
        )

    @staticmethod
    def execute(sql):
        try:
            cursor = DatabaseClient.__database.cursor()
            cursor.execute(sql)
            cursor.close()
            DatabaseClient.__database.commit()
        except:
            return False
        return True

    @staticmethod
    def fetch(sql):
        try:
            cursor = DatabaseClient.__database.cursor()
            cursor.execute(sql)
            response = cursor.fetchall()
        except:
            return False
        return response

    @staticmethod
    def insert_into(table, fields, values):
        sql_command = f'INSERT INTO {table} ({fields}) VALUES ({values})'
        print(sql_command)
        DatabaseClient.execute(sql_command)

    @staticmethod
    def update(table, values, condition):
        sql_command = f'UPDATE {table} SET {values} WHERE {condition}'
        print(sql_command)
        DatabaseClient.execute(sql_command)

    @staticmethod
    def select_from(table, fields='*', where=False):
        __where = ''
        if where is not False:
            __where = f'WHERE {where}'
        sql_command = f'SELECT {fields} FROM {table} {__where}'
        print(sql_command)
        result = DatabaseClient.fetch(sql_command)
        return result

    @staticmethod
    def close(DatabaseClient):
        DatabaseClient.__database.close()