from pymongo import MongoClient

class DatabaseClient:
    __URI = 'mongodb://localhost:27017'
    __database = None

    @staticmethod
    def initialize(db_name):
        client = MongoClient(DatabaseClient.__URI)
        DatabaseClient.__database = client[db_name]

    @staticmethod
    def insert_one(collection, document):
        return DatabaseClient.__database[collection].insert_one(document)

    @staticmethod
    def insert_many(collection, documents):
        return DatabaseClient.__database[collection].insert_many(documents)

    @staticmethod
    def update(collection, query, data):
        new_values = { '$set': data }
        return DatabaseClient.__database[collection].update_one(query, new_values)

    @staticmethod
    def find(collection, query={}):
        return DatabaseClient.__database[collection].find(query)

    @staticmethod
    def find_one(collection, query={}):
        return DatabaseClient.__database[collection].find_one(query)

    @staticmethod
    def delete(collection, query):
        return DatabaseClient.__database[collection].delete_many(query)