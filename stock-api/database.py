import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv() # load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "carpart")

# create a mongodb client using the connection
client = MongoClient(MONGO_URI)

# get the database
db = client[MONGO_DB]

# collection which will store carpart's tools
products = db["products"]
