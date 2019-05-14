from pymongo import MongoClient
import os


class Database(object):
    # This class was made to create the bridge connection
    # between MongoDb and this application

    __db = None

    @classmethod
    def defineConnections(cls):
    # Singleton method to create the instatiate only 
    # one time the object belong to mongodb

        if cls.__db is None:
            # This method verify the environment which mongo is
            # and create the instance database 

            # Url of local Mongo and name of database
            url = 'mongodb://localhost:27017/'
            client_name = 'matriculaweb'

            # Verify the environment of Mongo ("production or local")
            if 'DB_URL' in os.environ:
                url = os.environ['DB_URL']

            # Verify if the mongo is in production and get the name there
            if 'DB_CLIENT_NAME' in os.environ:
                client_name = os.environ['DB_CLIENT_NAME']

            # Create the instance with MongoClient through the url
            client = MongoClient(url)
            cls.__db = client[client_name]

        return cls.__db

  