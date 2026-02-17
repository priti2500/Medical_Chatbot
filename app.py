"""
Medical AI Chatbot - Streamlit Web UI.
Run: streamlit run app.py
"""
import streamlit as st
import logging
from datetime import datetime

from config.settings import DISCLAIMER, CHAT_HISTORY_LIMIT
from src.chatbot import get_chatbot_chain, chat
from src.utils import setup_logging

# Optional: log to file for debugging (conversation history can be extended to file here)
setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for a cleaner, medical-themed UI
st.markdown("""
<style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .disclaimer-box {
        padding: 0.75rem 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .chat-message { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
    .user-msg { background: #e3f2fd; padding: 0.5rem 0.75rem; border-radius: 8px; margin-left: 2rem; }
    .bot-msg { background: #f5f5f5; padding: 0.5rem 0.75rem; border-radius: 8px; margin-right: 2rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag_chain():
    """Load RAG chain once and reuse across sessions. Returns (chain, None) or (None, error_msg)."""
    try:
        return get_chatbot_chain(), None
    except FileNotFoundError as e:
        logger.warning("Vector store not found: %s", e)
        return None, "vector_store"
    except ValueError as e:
        logger.warning("Config error: %s", e)
        return None, "api_key"
    except Exception as e:
        logger.exception("Failed to load RAG chain: %s", e)
        return None, "other"


def main():
    st.title("🩺 Medical AI Chatbot")
    st.caption("General health information assistant. Not a substitute for professional care.")

    # Sidebar: disclaimer and info
    with st.sidebar:
        st.header("Important")
        st.markdown(f'<div class="disclaimer-box">{DISCLAIMER}</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown("**How to use**")
        st.markdown("- Ask about symptoms, medications, or general health.")
        st.markdown("- Keep questions clear and short.")
        st.markdown("- For emergencies, call emergency services.")
        st.divider()
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.session_state.conversation_log = []
            st.rerun()

    # Initialize conversation state and log
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_log" not in st.session_state:
        st.session_state.conversation_log = []  # List of {role, content, timestamp}

    # Load RAG chain
    rag_result, load_error = load_rag_chain()
    if rag_result is None:
        st.error("Could not load the chatbot.")
        with st.expander("Setup steps (click to expand)", expanded=True):
            if load_error == "api_key":
                st.markdown("**1. Set your Groq API key**")
                st.markdown("- Open the `.env` file in the project folder.")
                st.markdown("- Set `GROQ_API_KEY=your-groq-api-key-here`.")
                st.markdown("- Get a key at: https://console.groq.com/keys")
                st.markdown("**2. Build the vector store** (in a terminal):")
                st.code("python scripts/build_vector_store.py", language="bash")
                st.markdown("**3. Restart this app** (stop and run `streamlit run app.py` again).")
            elif load_error == "vector_store":
                st.markdown("**1. Build the vector store** (in a terminal):")
                st.code("python scripts/build_vector_store.py", language="bash")
                st.markdown("Then **restart this app**.")
            else:
                st.markdown("**1. Create a `.env` file** if it does not exist.")
                st.markdown("**2. Set your Groq API key** in `.env`:")
                st.code("GROQ_API_KEY=your-groq-api-key-here", language="bash")
                st.markdown("Get a key at: https://console.groq.com/keys")
                st.markdown("**3. Build the vector store** (in a terminal):")
                st.code("python scripts/build_vector_store.py", language="bash")
                st.markdown("**4. Restart this app.**")
        st.stop()
    rag_chain = rag_result

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask a health-related question..."):
        # Append user message to UI and log
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_log.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build history for RAG (last N turns to stay within context window)
        history = []
        prev_messages = st.session_state.messages[:-1]  # Exclude current prompt
        if len(prev_messages) > CHAT_HISTORY_LIMIT:
            prev_messages = prev_messages[-CHAT_HISTORY_LIMIT:]
        for m in prev_messages:
            role = "user" if m["role"] == "user" else "assistant"
            history.append((role, m["content"]))

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply, error = chat(prompt, rag_chain, conversation_history=history)
            if error:
                st.error(error)
                reply = f"[Error: {error}]"
            else:
                st.markdown(reply)

        # Append assistant reply to state and log
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.conversation_log.append({
            "role": "assistant",
            "content": reply,
            "timestamp": datetime.utcnow().isoformat(),
        })


if __name__ == "__main__":
    main()
