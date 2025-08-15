import re
import unicodedata
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from bangla_pdf_ocr import process_pdf
from config import CHUNK_SIZE, CHUNK_OVERLAP

def normalize_bangla_text(text: str) -> str:
    """Normalize Bangla text and clean unwanted spaces, patterns."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(?:[অ-হ0-9০-৯,\s]+)\s[০-৯0-9]{1,4}\b", "", text)  # Remove book title/page no
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([।,.!?])", r"\1", text)
    text = re.sub(r"([।,.!?])\s+", r"\1 ", text)
    return text.replace("আইয়ূব", "আইয়ুব")

import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_document(pdf_path: str = None, txt_cache_path: str = None) -> str:
    """
    Load text from cache or process from PDF if cache is unavailable.
    Returns cleaned text as a string.
    """
    if txt_cache_path and not txt_cache_path.endswith(".txt"):
        raise ValueError("txt_cache_path must be a .txt file")

    # Try cache
    if txt_cache_path and os.path.exists(txt_cache_path):
        with open(txt_cache_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        if not pdf_path:
            raise FileNotFoundError(
                f"No text cache found at {txt_cache_path} and no PDF path provided."
            )
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Process PDF
        text = process_pdf(pdf_path)

        # Save to cache
        if txt_cache_path:
            with open(txt_cache_path, 'w', encoding='utf-8') as f:
                f.write(text)

    # Clean text
    return normalize_bangla_text(text)


def split_document(text: str, source_path: str = None):
    """
    Split cleaned text into chunks and return as list of Documents.
    """
    doc = Document(page_content=text, metadata={"source": source_path})
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["।", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents([doc])


# Example usage
# cleaned_text = load_document(pdf_path="file.pdf", txt_cache_path="file_cache.txt")
# docs = split_document(cleaned_text, source_path="file.pdf")
