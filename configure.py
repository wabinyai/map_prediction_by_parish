import os
from dotenv import load_dotenv
from pathlib import Path
 # Determine the path to the .env file
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"

def load_config():
    # Load environment variables from the .env file
    load_dotenv(dotenv_path)

    # Define a dictionary with default values
    config = {
        "PREDICT_URL": os.getenv("PREDICT_URL", "default_predict_url"),
        "TOKEN": os.getenv("TOKEN", "default_token"),
    }

    return config
