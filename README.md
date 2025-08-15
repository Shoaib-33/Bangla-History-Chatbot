# Bangla-History-Chatbot

<p align="center">
  <img src="static/sample_output.png" alt="Sample Output" width="600">
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

# Motivation
This project was inspired by an open-source initiative called "Real History of Bangladesh", which aims to preserve and present the authentic history of Bangladesh without distortion.
Building on that vision, I developed the entire AI-powered pipeline — from document processing, OCR, and text normalization to semantic search and context-aware question answering.

The goal is to make historical knowledge easily searchable in Bangla, ensuring both the questions and answers are in the native language, and that the answers are drawn only from verified historical documents.

This is an open-source effort and is completely free for improvement. Anyone interested in enhancing the dataset, improving accuracy, adding more models, or expanding features is welcome to contribute. Together, we can build a reliable, accessible, and truthful digital archive of Bangladesh’s history for future generations.
