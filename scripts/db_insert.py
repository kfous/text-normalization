import os
import pandas as pd
from pymongo import MongoClient
from text_normalizer import normalize_batch
from performance import calculate_performance
import timeit

if __name__ == "__main__":
    csv_path = '../dataset/normalization_assesment_dataset_10k.csv'
    client = MongoClient("mongodb://localhost:27017/")

    db = client["text_db"]
    collection = db["normalized_collection"]
    counter = 0
    start_time_10k = timeit.default_timer()
    print("Operation batch insert starting...")
    for chunk in pd.read_csv(csv_path, chunksize=100):
        start_time_500 = timeit.default_timer()

        raw_texts = chunk['raw_comp_writers_text'].tolist()

        normalized_texts = normalize_batch(raw_texts)

        if normalized_texts is not None:
            document = [{"normalized_text": text} for text in normalized_texts]
            collection.insert_many(document)
            counter += 1
            print(f"Batch {counter}: Inserted", flush=True)
        else:
            print("No data returned from normalizer")
        end_time_500 = timeit.default_timer()
        calculate_performance(start_time_500, end_time_500)

    end_time_10k = timeit.default_timer()
    calculate_performance(start_time_10k, end_time_10k)
