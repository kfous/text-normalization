"""""
As a second step you can further clean the data with an LLM model.
In this script llama3.1 of 8billion parameters and 4-quantiazation was used (based on my hardware specs)
""" ""

import timeit
import pandas as pd
from performance import calculate_performance
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv


def normalize_batch(raw_text):
    return [normalizer(line) for line in raw_text]


def normalizer(raw_text) -> str:
    load_dotenv()

    template = """Text: {text}
    1.Make a normalization to the provided text. 
    2.Remove unnecessary characters and provide ONLY the name and the surname of the person
    Your answer MUST include ONLY the name and the surname of the person. Be deterministic:
    Answer template:
    TheNames TheSurnames
    """

    # Load environment variables from the .env file.
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the model you want to use llama3/or deepseek-r1:7b and the base URL of the ollama running on your
    # localhost.
    model = OllamaLLM(
        model="llama3", base_url="http://localhost:11434", temprature=0.00001)

    # Create a chain of prompt template and model.
    chain = prompt | model

    # Prepare the question and invoke the model.
    try:
        res = chain.invoke({"text": raw_text})
        print(res)
        return res
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Load data
    csv_path = "../dataset/cleaned_data.csv"
    output_csv = "../dataset/ollama_cleaned_data/normalized_output.csv"

    chunk_size = 20

    # A flag used for the output csv, e.g. when true it will import headers
    first_chunk = True
    counter = 0
    # Performance variables saving current time
    start_time_10k = timeit.default_timer()
    print("Operation batch insert starting...")
    # Insert in chunks of 50 in database
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
