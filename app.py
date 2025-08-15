import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from preprocessing import load_document, normalize_bangla_text,split_document
from rag_builder import get_or_create_vectorstore, build_rag_pipeline
from models import QueryRequest, QueryResponse
from config import PDF_PATH, TEXT_PATH
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bangla-rag")

# Initialize FastAPI
app = FastAPI(title="বাংলাদেশ ইতিহাস বট", version="1.0.0")
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")

logger.info("Loading dataset & RAG pipeline...")
_cleaned_text = load_document(PDF_PATH, TEXT_PATH)
_docs = split_document(_cleaned_text, source_path=PDF_PATH or TEXT_PATH)
_vector_store = get_or_create_vectorstore(_docs)
_rag_chain = build_rag_pipeline(_vector_store)
logger.info("RAG system ready.")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_model=QueryResponse)
async def ask_question(payload: QueryRequest):
    if not payload.query.strip():
        return JSONResponse(status_code=400, content={"detail": "Query cannot be empty"})
    query_norm = normalize_bangla_text(payload.query)
    result = _rag_chain.invoke({"query": query_norm})
    answer = (result.get("result") or "").strip()
    return QueryResponse(answer=answer if answer else "উত্তর পাওয়া যায়নি")
