# Retrieval-Augmented Generation Examples

This folder contains educational notebooks showing how to build small RAG pipelines with persistent storage. The goal is to demonstrate how language models can use external knowledge bases for improved answers.

## What's Inside?

| Notebook | Summary |
|----------|---------|
| `basic_rag_with_chromadb.ipynb` | Minimal RAG pipeline using ChromaDB for document storage and retrieval. |
| `rag_with_multiple_search_modes.ipynb` | Compare similarity search strategies such as cosine similarity and maximal marginal relevance. |
| `graph_rag_basics.ipynb` | Simple graph-based RAG example using a knowledge graph. |

### Dependencies

These notebooks rely on the following libraries:

- `chromadb` for a persistent vector database.
- `sentence-transformers` or `openai` embeddings.
- `langchain` for RAG utilities.
- `networkx` or `neo4j` for graph examples.

Install everything with:

```bash
pip install chromadb sentence-transformers langchain openai networkx neo4j
```

Some notebooks may require API keys for certain embedding or LLM services. Refer to the comments inside each notebook.

## Classic RAG vs Graph RAG

Classic RAG retrieves semantically similar documents from a vector store and feeds them to an LLM. Graph RAG also reasons over relationships in a knowledge graph before querying the language model. This can improve precision for structured data like research papers or organizational charts.

Use these notebooks as starting points for your own retrieval pipelines.
