# openai/data/db_mongo.py

import os
from pymongo import MongoClient

def get_mongo_conn():
    """
    Establish and return a connection to MongoDB 
    using environment variables for configuration.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client
