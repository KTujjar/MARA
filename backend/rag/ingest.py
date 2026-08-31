from langchain_community.document_loaders import DirectoryLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chroma_store import vectorstore
from pathlib import Path

def run_ingestion():
    BASE_DIR = Path(__file__).resolve().parent  # wherever ingest.py itself physically lives

    loader = DirectoryLoader(str(BASE_DIR / "documents"))
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")   # <- add this
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")  # <- and this
    vectorstore.add_documents(chunks)

def get_all():
    all_docs = vectorstore.get()
    print(f"Total chunks: {len(all_docs['documents'])}")
    for doc in all_docs['documents'][:5]:
        print(doc[:100], "\n---")


if __name__ == "__main__":
    #run_ingestion()
    get_all()

