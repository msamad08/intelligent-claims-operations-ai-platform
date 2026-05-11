from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "documents"
VECTOR_DIR = BASE_DIR / "vectorstore"


def load_pdf_documents():
    documents = []

    for pdf_file in DOCS_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = pdf_file.name

        documents.extend(docs)

    return documents


def main():
    documents = load_pdf_documents()

    if not documents:
        print("No PDF documents found in data/documents.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR)
    )

    print(f"Loaded {len(documents)} pages.")
    print(f"Created {len(chunks)} chunks.")
    print(f"Vector database saved to {VECTOR_DIR}")


if __name__ == "__main__":
    main()