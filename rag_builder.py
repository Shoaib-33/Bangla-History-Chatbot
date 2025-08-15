import os
import logging
from config import GOOGLE_API_KEY, COLLECTION_NAME, CHROMA_DB_DIR
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="l3cube-pune/bengali-sentence-similarity-sbert",
        encode_kwargs={'normalize_embeddings': True}
    )

def get_or_create_vectorstore(docs):
    embeddings = get_embeddings()
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    if len(vector_store.get().get('ids', [])) == 0:
        logger.info("Creating Chroma DB...")
        vector_store = Chroma.from_documents(
            docs, embeddings,
            persist_directory=CHROMA_DB_DIR,
            collection_name=COLLECTION_NAME
        )
        vector_store.persist()
    return vector_store

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,
        max_output_tokens=512
    )

def build_rag_pipeline(vector_store):
    llm = get_llm()
    prompt = PromptTemplate(
        template="""
        তুমি বাংলা সাহিত্যের বিশেষজ্ঞ। কেবল নিম্নোক্ত প্রসঙ্গ (context) থেকেই উত্তর দাও।
        যদি প্রসঙ্গে উত্তর না থাকে, শুধু লিখবে: "উত্তর পাওয়া যায়নি"।
        প্রসঙ্গ:
        {context}
        প্রশ্ন: {question}
        উত্তর:
        """,
        input_variables=["context", "question"]
    )
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 12, "fetch_k": 60, "lambda_mult": 0.3}
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
