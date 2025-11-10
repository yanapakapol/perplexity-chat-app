import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
api_key = os.getenv("PERPLEXITY_API_KEY")
print("API Key loaded:", api_key)
