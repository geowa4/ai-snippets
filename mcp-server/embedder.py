"""Create embeddings ."""

import logging
from pathlib import Path

import chromadb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def init_collection() -> chromadb.Collection:
    """Return the Chromadb client with fresh storage."""
    storage_path = Path.home() / ".chroma"

    # Delete existing storage if it exists
    if storage_path.exists():
        import shutil

        logger.info("Removing existing storage: %s", storage_path)
        shutil.rmtree(storage_path)

    storage_path.mkdir(exist_ok=True)

    chroma_client = chromadb.PersistentClient(path=str(storage_path.absolute()))
    return chroma_client.get_or_create_collection(name="ai-snippet-readme")


def add_doc(collection: chromadb.Collection, identifier: str, document: str) -> None:
    """Add to the Chromadb collection."""
    collection.add(
        ids=[identifier],
        documents=[document],
    )


def process_summaries(root_dir: Path) -> chromadb.Collection:
    """Process all SUMMARY.md files in subdirectories and add them to chromadb."""
    logger.info("Processing summary files in %s", root_dir)
    collection = init_collection()

    readme_files = root_dir.glob("*/SUMMARY.md")

    for readme_path in readme_files:
        content = readme_path.read_text(encoding="utf-8")
        identifier = readme_path.parent.name
        add_doc(collection, identifier, content)
        logger.info("Added %s to collection", identifier)

    return collection


def test_query(collection: chromadb.Collection, query_text: str, n_results: int = 2) -> dict:
    """Run a test query against the collection and return results."""
    results = collection.query(
        query_texts=[query_text],  # multiple queries supported but only making one
        n_results=n_results,
    )

    # the index below matches the query index; we only have 1 query.
    logger.info("Query result IDs: %s", results.get("ids", [[]])[0])
    for result in results.get("documents", [[]])[0]:
        logger.info("Query result: %s", result.splitlines()[0])
    return results


def main() -> None:
    """Entry point for the script."""
    import sys

    num_args = 2
    if len(sys.argv) != num_args:
        logger.error("Missing directory argument")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.exists() or not directory.is_dir():
        logger.error("Invalid directory: %s", directory)
        sys.exit(1)

    collection = process_summaries(directory)

    test_query(collection, "rag")


if __name__ == "__main__":
    main()
