import pandas as pd
import tiktoken


# Encoding cl100k_base for GPT model used
def count_tokens(text, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


# Calculate cost based on token count
def calculate_cost(token_count, price_per_1k_tokens):
    return (token_count / 1000) * price_per_1k_tokens


if __name__ == "__main__":
    # Create a DataFrame for token counts
    df = pd.read_csv("../dataset/raw_data.csv")
    df["raw_comp_writers_text"] = df["raw_comp_writers_text"].fillna("").astype(str)
    df["token_count"] = df["raw_comp_writers_text"].apply(count_tokens)

    # Calculate the total tokens
    total_tokens = df["token_count"].sum()

    # GPT 3.5 Turbo pricing
    input_price_per_1k_tokens = 0.0015
    output_price_per_1k_tokens = 0.002

    # Calculate the cost for input and output
    input_cost = calculate_cost(total_tokens, input_price_per_1k_tokens)
    output_cost = calculate_cost(total_tokens, output_price_per_1k_tokens)

    print("GPT 3.5-Turbo costs evaluation...")
    print(f"Total tokens: {total_tokens}")
    print(f"Estimated input cost: ${input_cost:.2f}")
    print(f"Estimated output cost: ${output_cost:.2f}")
