"""Database instance for the application."""
from pymongo import MongoClient

from app.core import configuration

if configuration.APP_ENVIRONMENT == "test":
    from mongomock import MongoClient as MockClient

    client = MockClient()
    db = client.get_database("test")
else:
    client = MongoClient(configuration.APP_MONGO_URI)
    db = client.get_database()
