import os
from dotenv import load_dotenv

load_dotenv()

# Data processing config
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 500
CHROMA_DB_DIR = "chroma_db"
PDF_PATH = ""
TEXT_PATH = "data/Bangla_History.txt"
COLLECTION_NAME = f"bangla_lit_v2_{CHUNK_SIZE}_{CHUNK_OVERLAP}"

# API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY missing from .env")
