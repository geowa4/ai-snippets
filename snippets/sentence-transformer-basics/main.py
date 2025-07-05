"""Demonstrate the use of sentence-transformers."""

import os

from sentence_transformers import SentenceTransformer

# If given a model name on huggingface (e.g. "Qwen/Qwen3-Embedding-8B"),
# it will download it.
# This may take a long time so you might want to download it first
# and pass the path to the folder.
# To download the model, ensure git-lfs is installed.
# Run `git lfs install`.
# Then clone the model.
#
# ```shell
# git clone https://huggingface.co/Qwen/Qwen3-Embedding-8B
# ````
#
# Because initiatlizing the model can take time,
# consider keeping this global so that is paid up front
# and not unexpectedly in the middle of a larger program.
model = SentenceTransformer(os.getenv("EMBEDDING_MODEL_OR_PATH"))


def main() -> None:
    """Run the demonstration code for sentence-transformers."""
    print("Model Details:")
    # print prompt prefixes, often "query" and "document" keys
    print(model.prompts)
    # print embedding dimension
    print(model.get_sentence_embedding_dimension())
    # print the name of the similarity function (e.g. "cosine")
    print(model.similarity_fn_name)

    # Sample data
    queries = [
        "What is the capital of China?",
        "Explain gravity",
    ]
    documents = [
        "The capital of China is Beijing.",
        (
            "Gravity is a force that attracts two bodies towards each other. "
            "It gives weight to physical objects and "
            "is responsible for the movement of planets around the sun."
        ),
    ]

    # Encode sample queries and documents
    query_embeddings = model.encode_query(queries)
    document_embeddings = model.encode_document(documents)
    print(type(query_embeddings))
    similarity = model.similarity(query_embeddings, document_embeddings)  # type: ignore[arg-type]

    print("Indexed Similarities:")
    print(similarity)
    print(float(similarity[0][0]))


if __name__ == "__main__":
    main()
