# LLM Memory Demo

This document explains how `llm_memory_demo.py` uses a simple external store to simulate long‑term memory when chatting with a model served through **LM Studio**.

## Stateless vs. Stateful LLMs

Large language models are stateless by design: each request is independent and the model only considers the prompt you send. By persisting past interactions and adding the most relevant snippets back into the prompt, we can create the illusion of stateful, memory‑driven behavior.

## Memory in a RAG Pipeline

In retrieval‑augmented generation (RAG) pipelines, context retrieved from a knowledge base is combined with the user's current question. Conversation memory is just another source of context that can be appended to the prompt before calling the model.

```
[user question] + [retrieved docs] + [retrieved memory] -> LLM
```

## Short‑Term vs. Long‑Term Memory

- **Short‑term memory** is the model's context window. Anything outside that window is forgotten when the response is generated.
- **Long‑term memory** keeps a history in an external store (JSON or a database). Only the most relevant pieces are injected back into the context window for each request.

## Workflow Diagram

```
        +-------------+
        | User Input  |
        +------+------+      retrieve top-N
               |               memories
               v
       +-------+------+
       | Memory Store |<----+
       +-------+------+
               | write new
               | interaction
               v
     +---------+-----------+
     | Prompt Assembly      |
     +---------+-----------+
               |
               v
        +------+------+
        | LM Studio   |
        +-------------+
```

## Running the Script

Install the dependencies and start LM Studio so it exposes the HTTP API (by default on port 1234):

```bash
pip install requests sentence-transformers
python llm_memory_demo.py --model mistral
```

The script stores conversations in `memory.json`. Delete the file to start over or inspect it to see what the model "remembers".
