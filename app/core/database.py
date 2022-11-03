import pymongo

from app.core import configuration

client  = pymongo.MongoClient(configuration.APP_MONGO_URI)
db = client.get_database(configuration.APP_MONGO_DB)