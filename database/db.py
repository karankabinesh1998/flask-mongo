from pymongo import MongoClient
from config.constants import MONGODB_URI

# Establish MongoDB connection
def connect_to_mongodb():
    try:
        client = MongoClient(MONGODB_URI)
        return client
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None

# Close MongoDB connection
def close_mongodb_connection(client):
    try:
        client.close()
    except Exception as e:
        print("Error closing MongoDB connection:", e)

