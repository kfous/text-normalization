"""""
As a second step you can further clean the data with an LLM model.
In this script GPT 3.5-turbo which provided decent results.
""" ""
import time
import timeit
import regex
import pandas as pd

from logger import setup_logger
from performance import calculate_performance
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Init logger
logger = setup_logger("main_logger")


# Function responsible for calling normalizer per chunk size
def normalize_batch(raw_text):
    return [normalizer(line) for line in raw_text]


def normalizer(raw_text) -> str:
    load_dotenv()

    template = """
    Normalize the following text by extracting ONLY the full personal name. Follow these rules:
    1. Remove ALL special characters, numbers, and non-name content
    2. Preserve diacritics and capitalization of proper nouns
    3. Include all name components (given names, middle names, surnames)
    4. Format as: "[Firstnames] [Surnames]" with space separation
    5. Consider names from worldwide countries
    6. ONLY IF you encounter the word: **Unknown**  replace with word *N/A*
    7. Be deterministic
    
    Examples:
    Input: "**Jorge@Luis_Borges_123" → Output: "Jorge Luis Borges"
    Input: "MARÍA-DELA; López" → Output: "María Dela López"
    
    Text: {text}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are a text normalization expert specialized in name extraction."
            ),
            HumanMessage(content=template.format(text=raw_text)),
        ]
    )
    # Initialize the model you want to use
    model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Create a chain of prompt template and model.
    chain = prompt | model

    max_retries = 3
    attempt = 0

    if not raw_text:
        return ""
    MAX_NAME_LENGTH = 150  # ~120 was the biggest value
    # A pattern which checks for an output: <A name>
    # Taking notice for all possible scenarios, like the name will be in "" or '' or **
    INVALID_OUTPUT_PATTERN = regex.compile(
        r'^output:\s*["\'*]*n\/a["\'*]*$', regex.IGNORECASE
    )
    while attempt < max_retries:
        try:
            response = chain.invoke({"text": raw_text})
            content = response.content.strip()
            if INVALID_OUTPUT_PATTERN.match(content.casefold()):
                return "N/A"
            # Check length
            if len(content) < MAX_NAME_LENGTH:
                # logger.info(content)
                return content
            # if it didn't succeed start a retry mechanism
            # logger.info(
            #     f"Wrong content: '{content}' | Attempt {attempt + 1} of {max_retries}. Retrying..."
            # )
            attempt += 1
            # A retry mechanism showcasing my eagerness to get the best result
            # if the result isn't what we want retry max 3 times, with a little greater temprature
            # and a backoff wait time to ensure the service doesn't consider us as a spam
            if attempt <= max_retries:
                chain = prompt | model.with_config(temperature=0.3)
                backoff_time = min(attempt * 1, 2)
                # logger.info(f"Waiting {backoff_time}s before retry...")
                time.sleep(backoff_time)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            attempt += 1
    # logger.info("N/A")
    return "N/A"


if __name__ == "__main__":
    # Load data
    csv_path = "../dataset/cleaned_data.csv"
    output_csv = "../dataset/openai_cleaned_data/normalized_output.csv"

    # Pick a chunk size to process the dataset information
    # Chunk size will determine the batch process capacity
    CHUNK_SIZE = 100

    # A flag used for the output csv, e.g. when true it will import headers
    first_chunk = True
    counter = 0
    # Performance variables saving current time
    start_time_10k = timeit.default_timer()
    logger.info("Operation batch insert starting...")
    # Insert in chunks of 100 in database
    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE):
        start_time_500 = timeit.default_timer()

        # Replace empty values with string
        chunk["raw_comp_writers_text"] = (
            chunk["raw_comp_writers_text"].fillna("empty").astype(str)
        )

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
            logger.info(f"Batch {counter}: Inserted")
        else:
            logger.info("No data returned from normalizer")
        end_time_500 = timeit.default_timer()
        # Performance of batch
        calculate_performance(start_time_500, end_time_500)

    end_time_10k = timeit.default_timer()
    # Performance of all batches
    calculate_performance(start_time_10k, end_time_10k)
