import os
import pandas as pd
from pymongo import MongoClient
from text_normalizer import normalize_batch
from performance import calculate_performance
import timeit

if __name__ == "__main__":
    # Load data
    csv_path = "../dataset/cleaned_data.csv"
    output_csv = "../dataset/normalized_output.csv"

    client = MongoClient("mongodb://localhost:27017/")
    # Name of database and collection
    db = client["text_db"]
    collection = db["normalized_collection"]
    chunk_size = 100

    # A flag used for the output csv, e.g. when true it will import headers
    first_chunk = True
    counter = 0
    # Performance variables saving current time
    start_time_10k = timeit.default_timer()
    print("Operation batch insert starting...")
    # Insert in chunks of 100 in database
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        start_time_500 = timeit.default_timer()

        raw_texts = chunk["raw_comp_writers_text"].tolist()
        # Contains the cleaned texts
        normalized_texts = normalize_batch(raw_texts)

        if normalized_texts:
            # Append the normalized data to a new column of the csv
            chunk = chunk.assign(normalized_text=normalized_texts)
            # Write to CSV
            chunk.to_csv(
                output_csv,
                mode="a" if not first_chunk else "w",  # write mode
                header=first_chunk,
                index=False,  # no need to hold indexes
            )
            first_chunk = False
            # Prepare documents to insert the batch to MongoDB
            documents = [{"normalized_text": text} for text in normalized_texts]
            collection.insert_many(documents)
            counter += 1
            print(f"Batch {counter}: Inserted", flush=True)
        else:
            print("No data returned from normalizer")
        end_time_500 = timeit.default_timer()
        # Performance of batch
        calculate_performance(start_time_500, end_time_500)

    end_time_10k = timeit.default_timer()
    # Performance of all batches
    calculate_performance(start_time_10k, end_time_10k)
