import streamlit as st
from pathlib import Path
import subprocess
import sys

from rag_pipeline import answer_question

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "documents"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Intelligent Claims & Operations AI Assistant",
    layout="wide"
)

st.title("Intelligent Claims & Operations AI Assistant")

st.markdown("""
Enterprise RAG platform for insurance claims, SOP intelligence,
incident response guidance, and operational document retrieval.
""")

# ==========================
# PDF Upload Section
# ==========================

with st.sidebar:
    st.header("Document Management")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = DOCS_DIR / uploaded_file.name

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success("PDF(s) uploaded successfully.")

    if st.button("Rebuild Knowledge Base"):
        with st.spinner("Rebuilding vector database..."):
            subprocess.run(
                [sys.executable, str(BASE_DIR / "src" / "ingest_documents.py")],
                check=True
            )

        st.success("Knowledge base rebuilt successfully.")

# ==========================
# Chat Session State
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask a question about claims, operations, or incident procedures..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating response..."):
            conversation_history = ""

            for msg in st.session_state.messages[-6:]:
                conversation_history += f"{msg['role']}: {msg['content']}\n"

            result = answer_question(
                query=prompt,
                conversation_history=conversation_history
    )

            response_text = result["answer"]

            if result.get("sources"):
                response_text += "\n\n### Sources\n"

                for source in result["sources"]:
                    response_text += f"- {source}\n"

            if result.get("evidence"):
                response_text += "\n\n### Supporting Evidence\n"

                for item in result["evidence"]:
                    response_text += f"""
**Source:** {item['source']}

> {item['text']}

"""

            st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })