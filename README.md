<<<<<<< HEAD
# Medical AI Chatbot

A **Medical AI Chatbot** that uses a Large Language Model (LLM) with **Retrieval-Augmented Generation (RAG)** to answer general health questions. It is for **informational purposes only** and does not replace professional medical advice.

## Features

- **Natural language queries** – Users ask health-related questions in plain language.
- **RAG pipeline** – Retrieves relevant medical content from a vector store (FAISS) before generating answers.
- **Short, user-friendly responses** – Answers are kept brief and easy to understand.
- **Conversation history** – Session history is maintained in the UI and used for context.
- **Safety** – Disclaimers, input validation, and no dosing/prescription advice.
- **Web UI** – Streamlit interface for local or cloud deployment.

## Project Structure

```
Medical AI Chatbot/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Dev dependencies (e.g. pytest)
├── .env.example              # Template for environment variables
├── .gitignore
├── app.py                    # Streamlit web app entry point
├── config/
│   └── settings.py           # Configuration from env
├── data/
│   ├── raw/                  # Medical FAQs, text files (ingested)
│   │   └── medical_faqs.json # Sample FAQ data
│   └── processed/
├── src/
│   ├── ingest.py             # Load and chunk medical data
│   ├── embeddings.py         # Embeddings and FAISS vector store
│   ├── rag.py                # RAG chain (retrieve + generate)
│   ├── chatbot.py            # Chat logic, disclaimers, logging
│   └── utils.py              # Validation and error handling
├── scripts/
│   ├── build_vector_store.py # Ingest data and build FAISS index
│   └── test_queries.py       # Example test queries (CLI)
├── tests/
│   ├── test_utils.py
│   └── test_ingest.py
├── docs/
│   ├── SETUP.md              # Setup and vector DB / API keys
│   ├── DEPLOYMENT.md         # Local and cloud deployment
│   ├── TESTING.md            # How to test and example queries
│   └── SECURITY.md           # Security and safety guidelines
└── vector_store/             # FAISS index (created by script; in .gitignore)
```

## Quick Start

1. **Clone and install**
   ```bash
   cd "Medical AI Chatbot"
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

2. **Configure**
   - Create a `.env` file in the project root (or copy from `.env.example` if present).
   - Set your Groq API key in `.env` (required for the LLM):
     ```env
     GROQ_API_KEY=your-groq-api-key-here
     ```

3. **Build vector store**
   ```bash
   python scripts/build_vector_store.py
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Open the URL shown in the terminal (e.g. http://localhost:8501).

5. **Optional: run tests**
   ```bash
   pip install -r requirements-dev.txt
   pytest tests/ -v
   ```

For detailed setup (vector DB options, API keys), see [docs/SETUP.md](docs/SETUP.md).  
For deployment (local and cloud), see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).  
For testing and example queries, see [docs/TESTING.md](docs/TESTING.md).  
For security and safety, see [docs/SECURITY.md](docs/SECURITY.md).

## Tech Stack

- **Backend:** Python 3.9+
- **LLM & RAG:** LangChain + Groq (LLaMA) + HuggingFace embeddings
- **Vector store:** FAISS
- **UI:** Streamlit

## Disclaimer

This chatbot provides **general health information only** and is **not a substitute** for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions.
=======
# Medical_Chatbot
>>>>>>> 23a93be4bfdcb76cdd5f737e1c35d461d0c29ce6
