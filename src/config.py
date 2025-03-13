import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
        self.model_name = os.getenv("LLM_MODEL", "llama3-8b-8192")
        self.csv_file_path = os.getenv("CSV_FILE_PATH", "data/sample.csv")
        self.max_tokens = int(os.getenv("MAX_TOKENS", 1024))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))

    def get_groq_api_key(self):
        return self.groq_api_key

    def get_model_name(self):
        return self.model_name

    def get_csv_file_path(self):
        return self.csv_file_path

    def get_max_tokens(self):
        return self.max_tokens

    def get_temperature(self):
        return self.temperature

config = Config()