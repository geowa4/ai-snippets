# Chroma Vector Store

A Retrieval-Augmented Generation (RAG) application demonstrating document retrieval and query-based information fetching using LangChain, Ollama, and Chroma.

---

## 🎯 Purpose

This project demonstrates a basic RAG pipeline that:

1. Loads and chunks a Markdown document
2. Creates vector embeddings using Ollama's `bge-m3` model
3. Stores vectors in Chroma (in-memory for simplicity)
4. Performs semantic search to retrieve relevant information

---

## 🧱 Technologies Used

- **LangChain** - For building the RAG pipeline  
- **Ollama** - For generating embeddings using the `bge-m3` model  
- **Chroma** - Vector database for similarity searches  
- **MarkdownTextSplitter** - For splitting documents into manageable chunks  
- **Python 3.13+** - Required runtime  

---

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Ensure Ollama is Running

Make sure you have [Ollama](https://ollama.com/) installed and running locally. Pull the required model:

```bash
ollama pull bge-m3
```

### 3. Use Sample Document

A sample `rag.md` file is included in the project directory for demonstration purposes. You can replace it with your own content as needed.

---

## 🚀 Execution

Run the application with:

```bash
uv run python main.py
```

The script will:

1. Load and split the `rag.md` document into chunks  
2. Create embeddings and store them in an in-memory Chroma database  
3. Perform a semantic search for the query:  
   `"When is the RAG published?"`

---

## 📌 Example Output

```text
Created 1479 chunks from the document
Embeddings created and stored in Chroma

Query: When is the RAG published?

Top 3 matches:

1. Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00 per year...

2. The RaRa Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00...

3. RaRa Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00 per...
```

---

## 📝 Notes

- **In-memory storage**: This implementation uses Chroma's in-memory mode for simplicity. For production, consider persistent storage by adding a `persist_directory` parameter.
- **Model requirements**: Ensure the `bge-m3` model is available in Ollama before running the script.
- **Customization**: Modify the query or document content to test different scenarios.

---

## 🔧 Key Differences from Qdrant Implementation

This Chroma implementation offers several advantages over Qdrant:

- **Simpler Setup**: No need to manually configure vector dimensions or distance metrics
- **Built-in Integration**: Native LangChain integration with `langchain-chroma`
- **Automatic Configuration**: Chroma automatically handles embedding size detection
- **Streamlined API**: Fewer configuration steps required for basic usage

---

## 📁 Project Structure

```bash
chroma-vector-store/
├── main.py             # Core RAG pipeline implementation
├── pyproject.toml      # Dependency management
└── rag.md              # Sample input document (use or replace as needed)
```

---

## 🚦 Advanced Usage

### Persistent Storage

To enable persistent storage, modify the vector store creation:

```python
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="rag_documents",
    persist_directory="./chroma_db"  # Add this line
)
```

### Custom Embedding Models

Replace the Ollama embeddings with other providers:

```python
# OpenAI embeddings
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# HuggingFace embeddings
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

### Advanced Querying

Chroma supports various query methods:

```python
# Similarity search with scores
results_with_scores = vector_store.similarity_search_with_score(query, k=3)

# Maximum marginal relevance search
mmr_results = vector_store.max_marginal_relevance_search(query, k=3)

# Similarity search by vector
vector = embeddings.embed_query(query)
vector_results = vector_store.similarity_search_by_vector(vector, k=3)
```