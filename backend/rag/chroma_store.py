##Let the agent pull from a local socument set (PDFs, notes) using Chroma
##Embedded vector store via LangChain.
##Keep it simple: ingest, embed, retrieve top-k chunks, inject into the prompt


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=str(BASE_DIR / "chroma_db"),
)

