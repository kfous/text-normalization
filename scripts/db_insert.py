import os
from pymongo import MongoClient
from text_normalizer import normalizer

if __name__ == "__main__":

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
    client = MongoClient(MONGO_URI)

    db = client["text_db"]
    collection = db["normalized_collection"]

    data = normalizer()
    if data is not None:
        document = {"normalized_text": data}
        collection.insert_one(document)
    else:
        print("No data returned from normalizer")
