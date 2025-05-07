#! /usr/bin/env python3

"""Demonstrate how to load markdown files and store them in a vector store."""

from langchain.text_splitter import MarkdownTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models


def load_and_chunk_document(file_path: str) -> list[Document]:
    """Load and chunk the markdown document."""
    loader = TextLoader(file_path)
    documents = loader.load()

    # Create a markdown splitter
    markdown_splitter = MarkdownTextSplitter(
        chunk_size=200,
        # chunk_size=1000,  # experiment with different values  # noqa: ERA001
        # chunk_overlap=200,  # noqa: ERA001
    )

    # Split the documents
    return markdown_splitter.split_documents(documents)


def create_embeddings(chunks: list[Document]) -> QdrantVectorStore:
    """Create embeddings and store them in Qdrant."""
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model="bge-m3")

    # Determine embedding size by creating a test embedding
    embedding_size = len(embeddings.embed_query("test"))
    print(f"Embedding size: {embedding_size}")

    # Initialize Qdrant client
    client = QdrantClient(":memory:")  # Using in-memory storage for this example

    # Create a new collection
    client.create_collection(
        collection_name="rag_documents",
        vectors_config=models.VectorParams(
            size=embedding_size,  # Use the determined size
            distance=models.Distance.COSINE,
        ),
    )

    # Create vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag_documents",
        embedding=embeddings,
    )

    # Add documents to the vector store
    vector_store.add_documents(chunks)

    return vector_store


def query_documents(
    vector_store: QdrantVectorStore,
    query: str,
    k: int = 3,
) -> list[str]:
    """Query the vector store for similar documents."""
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


def main() -> None:
    """Load & chunk document, store chunks in the vector database, and query to test."""
    # Load and chunk the document
    chunks = load_and_chunk_document("rag.md")
    print(f"Created {len(chunks)} chunks from the document")

    # Create embeddings and store in Qdrant
    vector_store = create_embeddings(chunks)
    print("Embeddings created and stored in Qdrant")

    # Example query
    query = "When is the RAG published?"
    results = query_documents(vector_store, query)

    print("\nQuery:", query)
    print("\nTop 3 matches:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result[:500]}...")  # Print first 500 characters of each result


if __name__ == "__main__":
    main()
