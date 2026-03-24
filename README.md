# Conversational Real Estate Search

An AI-powered system that converts natural language queries into structured database queries for real estate search.

## 🚀 Features

- Natural language → SQL query conversion
- LLM-based entity extraction (~95% accuracy)
- Query guard to filter irrelevant inputs
- Modular pipeline (normalization → mapping → query → execution)
- PostgreSQL integration
- Semantic search experimentation using FAISS + Sentence Transformers

## 🧠 Tech Stack

- Python
- spaCy (NER, Entity Ruler) (First iteration)
- LLMs (LLaMA / Qwen via Ollama)
- PostgreSQL (psycopg2)
- FAISS / Sentence Transformers
- LangChain / LangGraph (experimentation)

## 🏗️ Architecture

User Query → Entity Extraction → Normalization → Canonical Mapping → SQL Builder → DB Execution → LLM Response

## 📌 Key Highlights

- Improved entity extraction accuracy from **~50% → ~95%**
- Designed a modular and scalable query pipeline
- Explored vector search for semantic matching

## 📂 Future Improvements

- Full semantic search integration (Milvus)
- Hybrid LLM + deterministic query planner
- Ranking & personalization

---

## 📬 Author

Fardeen Shariff
