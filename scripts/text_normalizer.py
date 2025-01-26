from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv


def normalize_batch(raw_text):
    return [normalizer(line) for line in raw_text]


def normalizer(raw_text) -> str:
    load_dotenv()

    template = """Text: {text}
    Please make a normalization to the provided text. 
    Remove unnecessary characters and provide the ONLY the name and the surname of the person
    Answer like:
    <Name Surname>
    """

    # Load environment variables from the .env file.
    prompt = ChatPromptTemplate.from_template(template)  # Create a prompt template.

    # Initialize the model you want to use llama3/or deepseek-r1:7b and the base URL of the ollama running on your
    # localhost.
    model = OllamaLLM(model="llama3.1:8b-instruct-q4_0", base_url='http://localhost:11434')

    # Create a chain of prompt template and model.
    chain = prompt | model

    # Prepare the question and invoke the model.
    try:
        res = chain.invoke({"text": raw_text})
        return res
    except Exception as e:
        print(f"An error occurred: {e}")
