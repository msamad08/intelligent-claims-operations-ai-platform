from pathlib import Path
from dotenv import load_dotenv
import re
from langchain_ollama import ChatOllama

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vectorstore"


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=str(VECTOR_DIR),
        embedding_function=embeddings
    )


def retrieve_documents(query: str, k: int = 4):
    vectorstore = load_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return docs


def clean_text(text: str) -> str:

    # remove excessive whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    # remove weird spaced letters like:
    # c r i t i c a l
    text = re.sub(
        r'(?:(?<=\s)|^)(?:[A-Za-z]\s){3,}[A-Za-z](?=\s|$)',
        lambda m: m.group(0).replace(" ", ""),
        text
    )

    return text.strip()


def answer_question(query: str, conversation_history: str = ""):
    docs = retrieve_documents(query)

    if not docs:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    sources = list({
        doc.metadata.get("source", "Unknown source")
        for doc in docs
    })

    combined_text = " ".join([
        clean_text(doc.page_content) for doc in docs
    ])

    confidence = "High"
    escalation_required = "No"
    escalation_reason = ""

    if (
        "mold" in combined_text.lower()
        or "multiple carriers" in combined_text.lower()
        or "$25,000" in combined_text
        or "unclear policy" in combined_text.lower()
    ):
        escalation_required = "Yes"
        confidence = "Medium"
        escalation_reason = """
- Potential disputed coverage
- Multiple carrier involvement
- High estimated financial exposure
- Policy interpretation uncertainty
"""

    context_preview = "\n\n".join([
        clean_text(doc.page_content)[:1200]
        for doc in docs
    ])

    llm = ChatOllama(
        model="llama3.2",
        temperature=0.2
    )

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

    except Exception:
        generated_answer = f"""
    ### Retrieved Guidance

    Based on the uploaded documents, the most relevant guidance is:

    {context_preview[:1800]}

    ### Recommended Next Step

    For high-risk claims, coverage disputes, unclear policy language, or operational uncertainty, escalate to a claims specialist or supervisor.

    Note: Local Ollama LLM was not available, so this response used retrieval-based fallback mode.
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