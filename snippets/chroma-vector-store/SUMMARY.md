# Chroma Vector Store

This project is built in Python and demonstrates a Retrieval-Augmented Generation (RAG) pipeline that processes documents, creates vector embeddings, and performs semantic searches using Chroma as the vector database.
Chroma Vector Store serves as a practical example of how to implement document retrieval and query-based information fetching for applications needing contextual responses to natural language queries, with simplified setup compared to other vector databases.

## Technologies Used

- **Python 3.13+** - Core programming language
- **LangChain** - Framework for building RAG pipelines
- **Ollama** - Embedding model provider using the bge-m3 model
- **Chroma** - Vector database for storing and retrieving embeddings with simplified configuration
- **MarkdownTextSplitter** - Tool for chunking documents into manageable pieces

## Key Features

- **In-memory vector storage** - Fast setup for development and testing
- **Automatic embedding configuration** - No manual vector dimension setup required
- **Native LangChain integration** - Streamlined API through langchain-chroma
- **Semantic document search** - Query documents using natural language
- **Modular design** - Easy to extend and customize for different use cases