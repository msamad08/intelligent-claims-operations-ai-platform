from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from rag_pipeline import EMBEDDING_MODEL

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "data" / "documents"
VECTOR_DIR = BASE_DIR / "vectorstore"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_pdf_documents():
    documents = []

    for pdf_file in DOCS_DIR.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = pdf_file.name

            documents.extend(docs)
            print(f"Loaded: {pdf_file.name} ({len(docs)} pages)")

        except Exception as e:
            print(f"Failed to load {pdf_file.name}: {e}")
            continue

    return documents


def main():
    print(f"Scanning: {DOCS_DIR}")

    documents = load_pdf_documents()

    if not documents:
        print("No PDF documents found in data/documents/")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages.")

    print("Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Building vector database...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR)
    )

    print(f"Done. Vector database saved to {VECTOR_DIR}")


if __name__ == "__main__":
    main()