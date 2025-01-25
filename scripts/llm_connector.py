from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


if __name__ == "__main__":

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama.llms import OllamaLLM
    from dotenv import load_dotenv

    # Define the template with placeholders for dynamic content.
    template = """Text: {text}
    Task: I will provide you a raw text which include Names. Please extract ONLY the name. Ignore any special character.
    Don't include your whole chain of thought.
    Answer like this:
    Final answer: <TheName>
    """

    if __name__ == "__main__":
        load_dotenv()  # Load environment variables from the .env file.
        prompt = ChatPromptTemplate.from_template(template)  # Create a prompt template.

        # Initialize the model specifying the model identifier and the API base URL.
        model = OllamaLLM(model="llama3", base_url="http://127.0.0.1:11434")

        # Create a chain of prompt template and model.
        chain = prompt | model

        # Prepare the question and invoke the model.
        try:
            res = chain.invoke({"text": "<Unknown>/Wright, Justyce Kaseem"})
            print(res)  # Print the model response.
        except Exception as e:
            print(f"An error occurred: {e}")
