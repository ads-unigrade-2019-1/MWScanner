from pymongo import MongoClient
import os


class Database:

    @staticmethod
    def defineConnections():

        url = 'mongodb://localhost:27017/'
        client_name = 'matriculaweb'

        if 'DB_URL' in os.environ:
            url = os.environ['DB_URL']

        if 'DB_CLIENT_NAME' in os.environ:
            client_name = os.environ['DB_CLIENT_NAME']

        client = MongoClient(url)
        db = client[client_name]

        return db
