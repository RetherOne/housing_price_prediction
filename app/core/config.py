import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


MODEL_PATH = os.getenv("MODEL_PATH")
if MODEL_PATH and not Path(MODEL_PATH).is_absolute():
    MODEL_PATH = BASE_DIR / MODEL_PATH
