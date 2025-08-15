# Bangla-History-Chatbot

<p align="center">
  <img src="sample_output.png" alt="Sample Output" width="600">
</p>


## 📜 Description

Bangla RAG QA is an AI-powered **Retrieval-Augmented Generation** (RAG) system built with **FastAPI** to **preserve and restore real Bangla history**.  
It can answer questions in Bangla using only trusted historical sources, ensuring that both the questions and answers remain fully in Bengali.

## 🎯 Main Aim

To create a **reliable digital archive of Bangla history** and make it searchable in natural Bangla language — no distortions, only facts from the original documents.

## 🛠 Tech Stack

- **Backend:** FastAPI  
- **OCR:** `bangla_pdf_ocr`  
- **Embeddings:** HuggingFace SBERT (Bangla)  
- **Vector Store:** ChromaDB  
- **LLM:** Groq / Gemini / OpenAI via LangChain  
- **Text Processing:** Unicode normalization & Bangla-specific cleanup
