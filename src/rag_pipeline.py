from pathlib import Path
from dotenv import load_dotenv
import os
import re

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from guardrails import evaluate, format_escalation_reasons

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Module-level cache
_vectorstore = None
_llm = None


def get_llm():
    global _llm

    if _llm is not None:
        return _llm

    openai_key = os.getenv("OPENAI_API_KEY")

    if openai_key:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    else:
        from langchain_ollama import ChatOllama
        _llm = ChatOllama(model="llama3.2", temperature=0.2)

    return _llm


def get_vectorstore():
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    _vectorstore = Chroma(
        persist_directory=str(VECTOR_DIR),
        embedding_function=embeddings
    )

    return _vectorstore


def retrieve_documents(query: str, k: int = 4):
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return docs


def clean_text(text: str) -> str:

    # Remove excessive whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    # Remove weird spaced letters like: c r i t i c a l
    text = re.sub(
        r'(?:(?<=\s)|^)(?:[A-Za-z]\s){3,}[A-Za-z](?=\s|$)',
        lambda m: m.group(0).replace(" ", ""),
        text
    )

    return text.strip()


def answer_question(query: str, conversation_history: str = ""):

    try:
        docs = retrieve_documents(query)
    except Exception as e:
        return {
            "answer": f"Could not access the knowledge base. Please ensure documents have been ingested first.\n\nError: {e}",
            "sources": [],
            "evidence": []
        }

    if not docs:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": [],
            "evidence": []
        }

    sources = list({
        doc.metadata.get("source", "Unknown source")
        for doc in docs
    })

    combined_text = " ".join([
        clean_text(doc.page_content) for doc in docs
    ])

    # Guardrails — escalation logic
    escalation = evaluate(combined_text)
    confidence = escalation.confidence
    escalation_required = "Yes" if escalation.escalation_required else "No"
    escalation_reason = format_escalation_reasons(escalation)

    context_preview = "\n\n".join([
        clean_text(doc.page_content)[:1200]
        for doc in docs
    ])

    llm = get_llm()

    prompt = f"""
You are an enterprise claims and operations intelligence assistant.

Use ONLY the provided retrieved document context.

Provide:
1. Concise operational guidance
2. Key documentation requirements
3. Escalation recommendations
4. Clear bullet points when appropriate

CONVERSATION HISTORY:
{conversation_history}

CURRENT QUESTION:
{query}

DOCUMENT CONTEXT:
{context_preview}

Provide a professional enterprise response.
"""

    try:
        response = llm.invoke(prompt)
        generated_answer = response.content

    except Exception as e:
        generated_answer = f"""
### Retrieved Guidance

Based on the uploaded documents, the most relevant guidance is:

{context_preview[:1800]}

### Recommended Next Step

For high-risk claims, coverage disputes, unclear policy language, or operational uncertainty,
escalate to a claims specialist or supervisor.

Note: LLM was not available ({e}), so this response used retrieval-based fallback mode.
"""

    answer = f"""
{generated_answer}

### Operational Assessment

- Confidence Level: {confidence}
- Escalation Required: {escalation_required}
"""

    if escalation_required == "Yes":
        answer += f"""
### Escalation Reasoning

{escalation_reason}
"""

    evidence = []
    seen_evidence = set()

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        text = clean_text(doc.page_content)[:350]
        key = (source, text[:120])

        if key not in seen_evidence:
            evidence.append({
                "source": source,
                "text": text
            })
            seen_evidence.add(key)

        if len(evidence) >= 3:
            break

    return {
        "answer": answer,
        "sources": sources,
        "evidence": evidence
    }