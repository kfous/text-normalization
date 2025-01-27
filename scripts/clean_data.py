"""""
First script in the cleaning process.
It will parse the original dataset and clean it:
1. Using a rule based approach with regex patterns
2. Using a NER validation to identify name entities
""" ""

import pandas as pd
import regex as re
import spacy
from tqdm import tqdm

# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


def rule_based_clean(name):
    # The placeholders I wanted to be removed
    PLACEHOLDERS = {
        "<unknown>",
        "unknown",
        "uknown" "traditional",
        "copyright control",
        "?",
        "will provide later",
        "not documented",
        "publisher unknown",
        "ascap",
        "socan",
        "bmi",
        "prodisc music company bmi",
        "zee music company",
        "administered by",
    }

    # Preserve parenthetical metadata
    preserved_metadata = []
    name = re.sub(
        r"\(([^)]+)\)",
        lambda m: (preserved_metadata.append(m.group(1)) or ""),
        name,
        flags=re.UNICODE,
    )

    # Clean core name components
    # Split first to handle component-level placeholders
    components = re.split(r"[/,&;]+", name)

    cleaned_components = []
    for comp in components:
        comp = re.sub(r"\s+", " ", comp.strip(), flags=re.UNICODE)
        comp = re.sub(r"[^\p{L}\p{M}0-9'’\-.()]", " ", comp, flags=re.UNICODE).strip()

        # Check against placeholders
        if comp.lower() in PLACEHOLDERS:
            continue  # Just skip it
        if comp:
            cleaned_components.append(comp)

    # Rebuild with standardized separators like a slash
    final_name = "/".join(cleaned_components)

    # Step 4: Reattach cleaned metadata
    if preserved_metadata:
        metadata_str = " ".join(f"({m})" for m in preserved_metadata)
        final_name = f"{final_name} {metadata_str}".strip()

    # Final normalization
    return re.sub(r"\s+", " ", final_name).strip()


def ner_validate(name):
    # Spacy model will label for me potential PERSON ORG or GPE
    components = name.split("/")
    valid_components = []
    for comp in components:
        doc = nlp(comp)
        # Check if component contains an entity
        has_valid_entity = any(
            ent.label_ in ("PERSON", "ORG", "GPE") for ent in doc.ents
        )
        # If no entity found but text looks name-like (title case), keep it
        if has_valid_entity or (comp.istitle() and len(comp.split()) >= 1):
            valid_components.append(comp)
    return "/".join(valid_components) if valid_components else "Unknown"


def clean_dataset_column(df, column_name):
    # A nice library to show the progress
    tqdm.pandas(desc="Cleaning names")
    # Rule-based cleaning
    df[column_name] = df[column_name].astype(str).progress_apply(rule_based_clean)
    # NER validation
    df[column_name] = df[column_name].progress_apply(ner_validate)
    return df


# Example usage
if __name__ == "__main__":
    # Load data
    input_file = "../dataset/raw_data.csv"
    output_file = "../dataset/cleaned_data.csv"
    df = pd.read_csv(input_file)

    # Clean the target column
    df = clean_dataset_column(df, column_name="raw_comp_writers_text")

    # Save results
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
