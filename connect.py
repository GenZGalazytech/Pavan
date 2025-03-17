from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
db = client.Pixelhub
users_collection = db.users
image_collection = db.images

AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_database():
    return db

def get_users_collection():
    return users_collection

def get_image_collection():
    return image_collection