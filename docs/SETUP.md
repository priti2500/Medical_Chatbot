# Setup Instructions

## 1. Python Environment

- **Python 3.9 or higher** is recommended.
- Create and activate a virtual environment:

  **Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```

  **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

  **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. API Keys

### OpenAI (required)

The app uses **OpenAI** for:

- **Embeddings** (e.g. `text-embedding-3-small`) when building the vector store.
- **Chat model** (e.g. `gpt-3.5-turbo`) for generating answers.

**Steps:**

1. Copy `.env.example` to `.env` in the project root.
2. Get an API key from [OpenAI API](https://platform.openai.com/api-keys).
3. In `.env`, set:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Important:** Never commit `.env` or share your API key. `.env` is listed in `.gitignore`.

### Optional: other LLM or embedding providers

The code is structured around OpenAI. To use another provider (e.g. Azure OpenAI, Anthropic), you would need to:

- Adjust `config/settings.py` for the new API key and model names.
- Swap the LangChain LLM/embedding classes in `src/rag.py` and `src/embeddings.py` to the appropriate LangChain integrations.

## 3. Vector Store

### Default: FAISS (local, no extra API key)

- **No sign-up** beyond OpenAI.
- Index is stored under `vector_store/faiss_index` (created when you run the build script).
- Suitable for local runs and small/medium datasets.

**Setup:**

1. Put your medical content in `data/raw/`:
   - **JSON:** list of objects with `question`, `answer`, and optional `category` (see `data/raw/medical_faqs.json`).
   - **Text/Markdown:** `.txt` or `.md` files.
2. Build the index:
   ```bash
   python scripts/build_vector_store.py
   ```
3. The app will load this index automatically when you run `streamlit run app.py`.

### Optional: Pinecone

- Create an account at [Pinecone](https://www.pinecone.io/).
- Create an index (e.g. dimension 1536 for `text-embedding-3-small`; check OpenAI embedding dimension).
- In `.env`:
  ```env
  VECTOR_STORE_TYPE=pinecone
  PINECONE_API_KEY=your-pinecone-api-key
  PINECONE_ENV=us-east-1
  PINECONE_INDEX_NAME=medical-chatbot
  ```
- The current code uses FAISS by default; adding Pinecone would require implementing a Pinecone vector-store path in `src/embeddings.py` (e.g. using `langchain_community.vectorstores.Pinecone`) and switching on `VECTOR_STORE_TYPE`.

### Optional: Weaviate

- Run Weaviate (e.g. Docker) and create a schema.
- In `.env`:
  ```env
  VECTOR_STORE_TYPE=weaviate
  WEAVIATE_URL=http://localhost:8080
  WEAVIATE_API_KEY=optional
  ```
- As with Pinecone, you would add a Weaviate vector-store implementation in `src/embeddings.py` and use it when `VECTOR_STORE_TYPE=weaviate`.

## 4. Environment Variables Summary

| Variable               | Required | Description                                  |
|------------------------|----------|----------------------------------------------|
| `OPENAI_API_KEY`       | Yes      | OpenAI API key for LLM and embeddings        |
| `VECTOR_STORE_TYPE`    | No       | `faiss` (default), or future: pinecone/weaviate |
| `VECTOR_STORE_PATH`    | No       | Path for FAISS index (default: vector_store/faiss_index) |
| `MAX_CONTEXT_DOCS`     | No       | Number of chunks to retrieve (default: 4)    |
| `LLM_MODEL`            | No       | OpenAI chat model (default: gpt-3.5-turbo)   |
| `EMBEDDING_MODEL`      | No       | OpenAI embedding model (default: text-embedding-3-small) |
| `CHAT_HISTORY_LIMIT`   | No       | Max messages in context (default: 20)        |

## 5. Verify Setup

1. **Vector store:** After running `python scripts/build_vector_store.py`, the folder `vector_store/faiss_index` should exist.
2. **App:** Run `streamlit run app.py` and open the URL; you should see the chatbot UI and disclaimer.
3. **CLI test:** Run `python scripts/test_queries.py` to run example queries (requires `.env` and built vector store).

If anything fails, check that:

- `OPENAI_API_KEY` is set in `.env`.
- You have run `build_vector_store.py` at least once.
- No firewall or proxy is blocking access to the OpenAI API.
