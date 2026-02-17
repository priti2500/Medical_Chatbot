"""
RAG pipeline: retrieve relevant chunks from the FAISS index and generate
answers with a Groq-hosted LLaMA model.
Uses LCEL (LangChain Expression Language) – no OpenAI dependency.
"""

import logging
from typing import List

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    MAX_CONTEXT_DOCS,
    MAX_RESPONSE_TOKENS,
)
from src.embeddings import load_faiss_index

logger = logging.getLogger(__name__)


SYSTEM_INSTRUCTION = """You are a helpful medical information assistant. Your role is to provide clear, short, and easy-to-understand information based on the context provided.

Rules:
- Answer only from the given context when possible. If the context does not contain enough information, say so and suggest the user consult a healthcare provider.
- Keep answers brief (2–4 short paragraphs max). Use simple language.
- Do not diagnose conditions or recommend specific treatments or dosages.
- Do not replace professional medical advice. When in doubt, advise seeing a doctor or pharmacist.
- End relevant answers with a short reminder that this is general information and not medical advice.
"""


# ✅ LLaMA from Groq
def get_llm() -> ChatGroq:
    """Create Groq LLaMA chat model (no OpenAI)."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Add it to .env.")

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0.0,
        max_tokens=MAX_RESPONSE_TOKENS,
    )


def _format_docs(docs):
    """Turn retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vector_store: FAISS | None = None):
    """
    Build RAG chain using:
    Retriever -> Format Docs -> Prompt -> Groq LLaMA -> String Output
    """

    if vector_store is None:
        vector_store = load_faiss_index()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": MAX_CONTEXT_DOCS}
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_INSTRUCTION + "\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    llm = get_llm()

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: _format_docs(
                retriever.invoke(x["input"])
            ),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def format_chat_history(messages: List[tuple]) -> List:
    """Convert (role, content) into LangChain messages."""
    result = []
    for role, content in messages:
        if role == "user":
            result.append(HumanMessage(content=content))
        else:
            result.append(AIMessage(content=content))
    return result


def query_rag(
    question: str,
    rag_chain,
    chat_history: List[tuple] | None = None,
) -> dict:
    """
    Run RAG query with Groq LLaMA.
    Returns: {input, answer}
    """

    history = format_chat_history(chat_history or [])

    result = rag_chain.invoke({
        "input": question,
        "chat_history": history,
    })

    return {
        "input": question,
        "answer": result if isinstance(result, str) else result.content,
    }
