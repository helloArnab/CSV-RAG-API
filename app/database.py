from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

# uri = "mongodb+srv://{user}:{password}@csv-rag-api.uvoop9w.mongodb.net/?appName=csv-rag-api"

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

client = MongoClient("mongodb://localhost:27017/")
db = client["csv_rag"]
files_collection = db["files"]
rows_collection = db["rows"]

def insert_file(file_id: str, file_name: str):
    files_collection.insert_one({"_id": file_id, "file_name": file_name})

def insert_rows(rows: list):
    if rows:
        rows_collection.insert_many(rows)  # Bulk insert for efficiency

def get_files():
    return list(files_collection.find({}, {"_id": 1, "file_name": 1}))

def get_rows_by_file_id(file_id: str):
    return list(rows_collection.find({"file_id": file_id}))

def delete_file(file_id: str):
    result = files_collection.delete_one({"_id": file_id})
    rows_collection.delete_many({"file_id": file_id})
    return result.deleted_count > 0