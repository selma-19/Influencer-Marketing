import configparser
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoConnection:
    _instance: Optional['MongoConnection'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            config = configparser.ConfigParser()
            config.read('../config.ini')
            cls.mongo_config = config['MongoDB']  # Access the MongoDB section
            cls.host = cls.mongo_config.get("HOST", "localhost")
            cls.port = int(cls.mongo_config.get("PORT", 27017))
            cls.database_name = cls.mongo_config.get("DB_NAME", "InfluencersMarketing")
        try:
            # Creating client
            cls.client = MongoClient(cls.host, cls.port, serverSelectionTimeoutMS=5000)

            # Testing the connection
            cls.client.admin.command('ping')

            cls.database = cls.client[cls.database_name]
            cls.collection = cls.database[cls.mongo_config.get("INFLUENCERS_COLLECTION")]
            cls.posts = cls.database[cls.mongo_config.get("POSTS_COLLECTION")]

            print("MongoDB connection established")
        except ConnectionFailure as e:
            cls._instance = None
            print(f"Could not connect to MongoDB: {e}")

        return cls._instance

    def get_database(self):
        return self.database
