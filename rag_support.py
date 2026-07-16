"""Self-contained RAG helpers for the Streamlit Cloud deployment."""

import io
import os
import urllib.request

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROVIDERS = {
    "local": {
        "base_url": "http://localhost:11434/v1",
        "model": "hermes3:8b",
        "key": "ollama",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "key_env": "OPENROUTER_API_KEY",
    },
    "openai": {
        "base_url": None,
        "model": "gpt-4o-mini",
        "key_env": "OPENAI_API_KEY",
    },
}

EMBED_PROVIDERS = {
    "local": {
        "base_url": "http://localhost:11434/v1",
        "model": "nomic-embed-text",
        "key": "ollama",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "qwen/qwen3-embedding-8b",
        "key_env": "OPENROUTER_API_KEY",
    },
    "openai": {
        "base_url": None,
        "model": "text-embedding-3-small",
        "key_env": "OPENAI_API_KEY",
    },
}


def _key(config: dict) -> str:
    return config.get("key", "") or os.environ.get(config.get("key_env", ""), "")


def _local_available() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=0.5)
        return True
    except Exception:
        return False


def provider_available(provider: str) -> bool:
    return _local_available() if provider == "local" else bool(_key(PROVIDERS[provider]))


def embed_provider_available(provider: str) -> bool:
    return _local_available() if provider == "local" else bool(_key(EMBED_PROVIDERS[provider]))


@st.cache_resource
def get_client(provider: str):
    from openai import OpenAI

    config = PROVIDERS[provider]
    return OpenAI(base_url=config["base_url"], api_key=_key(config) or "none")


@st.cache_resource
def _embed_client(provider: str):
    from openai import OpenAI

    config = EMBED_PROVIDERS[provider]
    return OpenAI(base_url=config["base_url"], api_key=_key(config) or "none")


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    step = max(chunk_size - overlap, 20)
    chunks = []
    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks


@st.cache_resource
def build_index(chunks: tuple[str, ...]):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(chunks)
    return vectorizer, matrix


def _top_matches(query: str, chunks, vectorizer, matrix, top_k: int = 3):
    similarities = cosine_similarity(vectorizer.transform([query]), matrix)[0]
    indices = similarities.argsort()[::-1][:top_k]
    return [(int(i), chunks[i], float(similarities[i])) for i in indices]


@st.cache_data(show_spinner="임베딩 계산 중...")
def embed_texts(chunks: tuple[str, ...], provider: str) -> list[list[float]]:
    response = _embed_client(provider).embeddings.create(
        model=EMBED_PROVIDERS[provider]["model"], input=list(chunks)
    )
    return [item.embedding for item in response.data]


def search_docs_embed(query: str, chunks, chunk_vectors, provider: str, top_k: int = 3):
    response = _embed_client(provider).embeddings.create(
        model=EMBED_PROVIDERS[provider]["model"], input=[query]
    )
    similarities = cosine_similarity([response.data[0].embedding], chunk_vectors)[0]
    indices = similarities.argsort()[::-1][:top_k]
    return [(int(i), chunks[i], float(similarities[i])) for i in indices]


def _extract_pdf_text(file_bytes: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
