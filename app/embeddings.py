import chromadb
import logging
from sentence_transformers import SentenceTransformer

# Logger configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Initializing ChromaDB client
chroma_client = chromadb.PersistentClient(path="/data/chroma")

# Creating a collection to store vectors
collection = chroma_client.get_or_create_collection(name="rag_collection")

# Model for generating embeddings (vector)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def ass_document(text, doc_id):
    """Adding a document to the vector database."""
    try:
        embedding = embedding_model.encode(text)
        collection.add(documents=[text], embeddings=[embedding], ids=str([doc_id]))
    except Exception as e:
        logger.error(f"Error adding document {doc_id}: {e}")


def search_documents(query, top_k=3):
    """Searching for similar documents in the vector database."""
    try:
        query_embedding = embedding_model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        logger.error(f"Error searching document: {e}")
        return []
