from pymongo import MongoClient


class Database:

    @staticmethod
    def defineConnections():
        client = MongoClient('mongodb://localhost:27017/')
        db = client['matriculaweb']
        return db
        
