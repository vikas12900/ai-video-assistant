from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )

