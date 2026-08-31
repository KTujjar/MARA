from rag.chroma_store import vectorstore

#gets the query and gets the top 3(k) closes matches to the query
#from local docs
def search_local_docs(query: str, k: int = 3) -> str:
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in results)
