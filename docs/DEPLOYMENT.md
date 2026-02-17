# Deployment Instructions

## Running Locally

1. **Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure**
   - Copy `.env.example` to `.env`.
   - Set `OPENAI_API_KEY` in `.env`.

3. **Build vector store**
   ```bash
   python scripts/build_vector_store.py
   ```

4. **Start the app**
   ```bash
   streamlit run app.py
   ```
   Default URL: http://localhost:8501.

5. **Optional: bind to all interfaces**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

---

## Deploying to the Cloud

### Option A: Hugging Face Spaces (Streamlit)

1. Create a Space at [Hugging Face Spaces](https://huggingface.co/spaces) and choose **Streamlit** as SDK.
2. **Secrets:** In the Space → Settings → Variables and secrets, add:
   - `OPENAI_API_KEY`: your OpenAI API key.
3. **Vector store:** FAISS needs to be built and uploaded, or built at runtime:
   - **Option 1:** Run `build_vector_store.py` locally, then upload the `vector_store/` folder (e.g. `vector_store/faiss_index`) into the Space repo so the app can load it.
   - **Option 2:** In the Space’s `app.py`, add a startup step that runs `build_vector_store.py` if the index does not exist (slower first load).
4. **Requirements:** Add a `requirements.txt` in the Space repo (same as project’s `requirements.txt`).
5. **Entry:** Set the Space’s main file to `app.py` so Hugging Face runs `streamlit run app.py`.

**Note:** Do not put `.env` in the repo. Use Hugging Face secrets only.

---

### Option B: Render (Web Service)

1. Create a **Web Service** at [Render](https://render.com).
2. **Build:**
   - Build command: `pip install -r requirements.txt`
   - Optional: add a build step that runs `python scripts/build_vector_store.py` if you commit a pre-built `vector_store/` or generate it in the build.
3. **Start command:**
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
4. **Environment:** In Render dashboard, add environment variable `OPENAI_API_KEY`.
5. **Persistent storage:** Render’s disk is ephemeral. For a persistent FAISS index, use a pre-built index in the repo or an external store (e.g. S3 + download at startup).

---

### Option C: Vercel (with Streamlit)

Streamlit is not a first-class Vercel runtime. Options:

- **Use a backend + frontend split:** Run the Streamlit app on a service that supports long-lived processes (e.g. Render, Railway, HF Spaces) and, if needed, put a static or Next.js front on Vercel that talks to that backend.
- **Or:** Deploy the Streamlit app on **Railway**, **Fly.io**, or **Hugging Face Spaces** instead; they suit Streamlit better.

---

### Option D: Docker (run anywhere)

Example Dockerfile for local or cloud use:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Build vector store at build time (requires OPENAI_API_KEY at build if you want pre-built index)
# Or leave this to runtime and mount/volume vector_store
RUN python scripts/build_vector_store.py || true

ENV STREAMLIT_SERVER_PORT=8501
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build (with OpenAI key for building index):

```bash
docker build --build-arg OPENAI_API_KEY=sk-... -t medical-chatbot .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... medical-chatbot
```

Or use Docker Compose and pass `OPENAI_API_KEY` via env file.

---

## Checklist for Any Deployment

- [ ] `OPENAI_API_KEY` set via environment or secrets (never in code).
- [ ] Vector store available (FAISS index built and present, or built at startup).
- [ ] `requirements.txt` (and optional `requirements-dev.txt`) used for install.
- [ ] App listens on `0.0.0.0` and uses `PORT` if the platform provides it (e.g. Render).
- [ ] No `.env` or secrets committed; use the platform’s secret management.

For security and safety, see [SECURITY.md](SECURITY.md).
