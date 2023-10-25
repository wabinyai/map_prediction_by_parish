import os
from dotenv import load_dotenv
from pathlib import Path

# Determine the path to the .env file
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = os.path.join(BASE_DIR, ".env")

# Load environment variables from the .env file
load_dotenv(dotenv_path)

def load_config():
    return {
        "PREDICT_URL": os.environ.get("PREDICT_URL"),
        "TOKEN": os.environ.get("TOKEN"),
    }
