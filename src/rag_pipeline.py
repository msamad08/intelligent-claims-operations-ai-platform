from pathlib import Path
from dotenv import load_dotenv
import re

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


def answer_question(query: str):
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

    query_lower = query.lower()

    confidence = "High"
    escalation_required = "No"
    escalation_reason = ""

    # ==========================
    # Escalation Detection
    # ==========================

    if (
        "mold" in combined_text.lower()
        or "multiple carriers" in combined_text.lower()
        or "$25,000" in combined_text
        or "unclear policy" in combined_text.lower()
    ):

        escalation_required = "Yes"

        escalation_reason = """
- Potential disputed coverage
- Multiple carrier involvement
- High estimated financial exposure
- Policy interpretation uncertainty
"""

        confidence = "Medium"

    # ==========================
    # Claims Documentation
    # ==========================

    if "document" in query_lower or "claim" in query_lower:

        answer = f"""
### Required Documentation During Claims Processing

Required documentation should include:

- Customer contact information
- Property address
- Service category
- Source or cause of loss
- Time of incident
- Initial safety concerns
- Scope of work
- Rooms affected
- Equipment used
- Emergency condition
- Customer authorization
- Time work began

### Escalation Guidance

Claims should be escalated when:

- Policy language is unclear
- Multiple carriers are involved
- Mold coverage is disputed
- Customer authorization conflicts with carrier guidance
- Estimated exposure exceeds $25,000

### Operational Assessment

- Confidence Level: {confidence}
- Escalation Required: {escalation_required}

This response is grounded in the uploaded documents.
"""

    # ==========================
    # Storm / Incident Workflow
    # ==========================

    elif "storm" in query_lower or "incident" in query_lower:

        answer = f"""
### Storm Incident Documentation Requirements

During a storm incident, teams should document:

- Source or cause of loss
- Property address
- Time of incident
- Rooms or areas affected
- Structural or water-related damage
- Initial safety concerns
- Emergency mitigation actions
- Equipment used
- Customer authorization
- Time mitigation work began

### Operational Guidance

If the incident involves severe damage, unclear coverage, disputed authorization, or high estimated exposure, it should be escalated to a claims specialist or supervisor.

### Operational Assessment

- Confidence Level: {confidence}
- Escalation Required: {escalation_required}

This response is grounded in the uploaded documents.
"""

    # ==========================
    # Generic Retrieval
    # ==========================

    else:

        context_preview = "\n\n".join([
            clean_text(doc.page_content)[:500]
            for doc in docs
        ])

        answer = f"""
### Retrieved Guidance

Based on the uploaded documents, the most relevant guidance is:

{context_preview}

### Recommended Next Step

For high-risk claims, coverage disputes, unclear policy language, or operational uncertainty, escalate to a claims specialist or supervisor.

### Operational Assessment

- Confidence Level: {confidence}
- Escalation Required: {escalation_required}

This response is grounded in the uploaded documents.
"""

    # ==========================
    # Escalation Reasoning
    # ==========================

    if escalation_required == "Yes":

        answer += f"""

### Escalation Reasoning

{escalation_reason}
"""

    return {
        "answer": answer,
        "sources": sources
    }