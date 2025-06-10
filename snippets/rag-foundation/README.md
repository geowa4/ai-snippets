# RAG Foundation

A Retrieval-Augmented Generation (RAG) application demonstrating document retrieval and query-based information fetching using LangChain, Ollama, and Qdrant.

---

## 🎯 Purpose

This project demonstrates a basic RAG pipeline that:

1. Loads and chunks a Markdown document
2. Creates vector embeddings using Ollama's `bge-m3` model
3. Stores vectors in Qdrant (in-memory for simplicity)
4. Performs semantic search to retrieve relevant information

---

## 🧱 Technologies Used

- **LangChain** - For building the RAG pipeline  
- **Ollama** - For generating embeddings using the `bge-m3` model  
- **Qdrant** - Vector database for similarity searches  
- **MarkdownTextSplitter** - For splitting documents into manageable chunks  
- **Python 3.12+** - Required runtime  

---

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Ensure Ollama is Running

Make sure you have [Ollama](https://ollama.com/) installed and running locally. Pull the required model:

```bash
ollama serve
```

```bash
ollama pull bge-m3
```

Check the model installed
```bash
ollama list
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
2. Create embeddings and store them in an in-memory Qdrant database  
3. Perform a semantic search for the query:  
   `"When is the RAG published?"`

---

## 📌 Example Output

```text
Created 1479 chunks from the document
Embedding size: 1024
Embeddings created and stored in Qdrant

Query: When is the RAG published?

Top 3 matches:

1. Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00 per year...

2. The RaRa Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00...

3. RaRa Rag is published monthly except July  n the January edition of the Rag. and August by the Rochester Amateur Radio Association, P.O. Box 1388, Rochester, N.Y. 14603. Subscription price $1.00 per...
```

---

## 📝 Notes

- **In-memory storage**: This implementation uses Qdrant's in-memory mode (`:memory:`) for simplicity. For production, consider persistent storage.
- **Model requirements**: Ensure the `bge-m3` model is available in Ollama before running the script.
- **Customization**: Modify the query or document content to test different scenarios.

---

## 📁 Project Structure

```bash
rag-foundation/
├── main.py             # Core RAG pipeline implementation
├── pyproject.toml      # Dependency management
└── rag.md              # Sample input document (use or replace as needed)
```
