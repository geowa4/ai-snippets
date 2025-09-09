"""Demonstrate how to load markdown files and store them in a vector store."""

from langchain.text_splitter import MarkdownTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings


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


def create_embeddings(chunks: list[Document]) -> Chroma:
    """Create embeddings and store them in Chroma."""
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model="bge-m3")

    # Create vector store with in-memory storage
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="rag_documents",
    )


def query_documents(
    vector_store: Chroma,
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

    # Create embeddings and store in Chroma
    vector_store = create_embeddings(chunks)
    print("Embeddings created and stored in Chroma")

    # Example query
    query = "When is the RAG published?"
    results = query_documents(vector_store, query)

    print("\nQuery:", query)
    print("\nTop 3 matches:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result}")  # Print first 500 characters of each result


if __name__ == "__main__":
    main()
