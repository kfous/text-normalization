from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv
import os


def normalizer() -> str:
    load_dotenv()

    template = """Text: {text}
    Please make a normalization to the provided text. 
    Remove unnecessary characters and provide the ONLY the name and the surname of the person
    Answer like:
    <Name Surname>
    """

    # Load environment variables from the .env file.
    prompt = ChatPromptTemplate.from_template(template)  # Create a prompt template.
    base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

    # Initialize the model you want to use llama3/or deepseek-r1:7b and the base URL of the ollama running on your
    # localhost.
    model = OllamaLLM(model="llama3.1:8b-instruct-q4_0", base_url=base_url)

    # Create a chain of prompt template and model.
    chain = prompt | model

    # Prepare the question and invoke the model.
    try:
        res = chain.invoke({"text": "<Unknown>/Wright, Justyce Kaseem"})
        print(res)
        return res
    except Exception as e:
        print(f"An error occurred: {e}")
