"""Create embeddings ."""

from pathlib import Path

import chromadb


def get_collection() -> chromadb.Collection:
    """Return the Chromadb client."""
    storage_path = Path.home() / ".chroma"
    storage_path.mkdir(exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=str(storage_path.absolute()))
    return chroma_client.get_or_create_collection(name="ai-snippet-readme")


def add_doc(collection: chromadb.Collection, identifier: str, document: str) -> None:
    """Add to the Chromadb collection."""
    collection.add(
        ids=[identifier],
        documents=[document],
    )


def main() -> None:
    """Run a sample of chromadb."""
    collection = get_collection()
    add_doc(collection, "test1", "this is a test")
    add_doc(collection, "cast1", "of the emergency broadcast system")

    results = collection.query(
        query_texts=["system"],
        n_results=1,
    )
    print(results)


if __name__ == "__main__":
    main()
