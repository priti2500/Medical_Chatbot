# Testing the Medical AI Chatbot

## Unit Tests (pytest)

Run all tests:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Tests include:

- **tests/test_utils.py** – Input validation (`validate_query`), sanitization (`sanitize_for_display`).
- **tests/test_ingest.py** – Loading FAQ JSON and splitting documents.

Run a single file:

```bash
pytest tests/test_utils.py -v
```

## CLI Test Script (RAG + LLM)

After setting `OPENAI_API_KEY` and building the vector store:

```bash
python scripts/build_vector_store.py   # if not already done
python scripts/test_queries.py
```

This runs fixed example queries through the RAG pipeline and prints answers. Use it to confirm that retrieval and generation work before using the UI.

## Example Test Queries (for UI or CLI)

Use these in the web UI or adapt them in `scripts/test_queries.py`:

**Symptoms**

- What are common flu symptoms?
- What are signs of dehydration?
- When should I see a doctor for a headache?
- What could cause chest pain?

**Medication**

- Can I take ibuprofen with aspirin?
- What should I do if I miss a dose of my medicine?
- Can I drink alcohol while on antibiotics?

**General**

- How much water should I drink daily?
- What is normal blood pressure?
- How can I improve my sleep?

**Expected behavior**

- Answers should be short, in plain language, and based on the ingested content when possible.
- Each reply should include a disclaimer that the information is general and not medical advice.
- Queries asking for specific dosages or prescriptions should be rejected or redirected (see `src/utils.py` validation).

## Manual UI Testing

1. Start the app: `streamlit run app.py`.
2. Confirm the disclaimer is visible (e.g. in the sidebar).
3. Send a question; confirm you get a reply with a disclaimer footer.
4. Send an empty message or very long text; confirm you get a clear error or validation message.
5. Use “Clear conversation” and confirm history is reset.
6. Try a query that is outside the knowledge base; the bot should say it doesn’t have enough information and suggest consulting a healthcare provider.

## Error Handling to Check

- **Missing API key:** Start without `OPENAI_API_KEY`; app should show a clear error.
- **Missing vector store:** Delete or rename `vector_store/faiss_index`, then run the app; it should ask you to run `build_vector_store.py`.
- **Invalid input:** Empty string, only spaces, or query over 2000 characters; should get validation errors without crashing.

These steps cover basic correctness, safety behavior, and error handling for the Medical AI Chatbot.
