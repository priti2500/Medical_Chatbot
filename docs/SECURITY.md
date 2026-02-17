# Security & Safety Guidelines

## User Safety (Medical Disclaimer)

- **Informational only:** The chatbot is designed to provide general health information only. It must not be used as a substitute for professional medical advice, diagnosis, or treatment.
- **Disclaimers:**  
  - A clear disclaimer is shown in the UI (sidebar) and appended to every bot reply.  
  - Do not remove or weaken these disclaimers.
- **No prescribing:** The system does not prescribe medications or give specific dosages. Input validation blocks obvious dosage-seeking queries and redirects users to a doctor or pharmacist.
- **Escalation:** For emergencies or serious symptoms, users should be directed to seek immediate professional care or emergency services. The UI and docs should reinforce this.

## API Keys and Secrets

- **Never commit secrets:** Do not put `OPENAI_API_KEY` or any API key in code or in files committed to version control.
- **Use environment variables:** Store keys in `.env` (local) or in the deployment platform’s secret/variable store (e.g. Hugging Face secrets, Render env vars).
- **`.env` in `.gitignore`:** Ensure `.env` is listed in `.gitignore` and never committed.
- **Rotation:** If a key is exposed, revoke it and create a new one in the provider’s dashboard.

## Data and Privacy

- **No PII in logs:** Avoid logging user messages or identifiable data in production. Conversation history in the app is in-memory (session) only unless you explicitly add logging.
- **Medical data:** Any medical FAQs or content you ingest should be from trusted, legally appropriate sources and compliant with your use case and jurisdiction.
- **Vector store:** The FAISS index is built from your ingested data. Store it in a secure location and do not expose it to untrusted users if it contains sensitive content.

## Input Validation and Error Handling

- **Validation:** User input is validated in `src/utils.py` (length, type, blocked patterns). Keep these checks and extend them if you add new entry points.
- **Errors:** The app catches errors in the RAG/chat flow and returns user-friendly messages instead of stack traces. Do not expose internal details or API keys in error responses.
- **Dependency updates:** Periodically update dependencies (`pip install -U -r requirements.txt`) and review security advisories for LangChain, OpenAI, and other packages.

## Deployment Security

- **HTTPS:** Use HTTPS in production so traffic to the chatbot is encrypted.
- **Secrets in cloud:** Use the platform’s secret management (e.g. Hugging Face secrets, Render env vars). Do not pass secrets via URL or frontend.
- **Access control:** If you need access control, add authentication (e.g. login) or restrict access (e.g. VPN, IP allowlist) at the deployment layer; the current code does not implement auth.

## Summary Checklist

- [ ] Disclaimers always visible and appended to answers.
- [ ] No API keys in code or in committed files.
- [ ] `.env` in `.gitignore` and used only locally; cloud uses platform secrets.
- [ ] User input validated; no sensitive data in logs.
- [ ] Dependencies updated; deployment uses HTTPS and secure secret handling.

Following these guidelines helps keep the Medical AI Chatbot safe and secure for informational use.
