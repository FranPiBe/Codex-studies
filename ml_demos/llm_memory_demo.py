import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

import requests

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None
    util = None

API_URL = "http://localhost:1234/v1/chat/completions"


def load_history(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(path: str, history: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def retrieve_context(query: str, history: List[Dict[str, Any]], model: Any, top_k: int) -> List[Dict[str, Any]]:
    if not history:
        return []
    if model and util:
        query_vec = model.encode(query)
        scored = []
        for item in history:
            if item.get("embedding") is not None:
                score = float(util.cos_sim(query_vec, item["embedding"]))
                scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]
    return history[-top_k:]


def build_messages(system_prompt: str, context: List[Dict[str, Any]], user_input: str) -> List[Dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for item in context:
        messages.append({"role": "user", "content": item["user"]})
        messages.append({"role": "assistant", "content": item["assistant"]})
    messages.append({"role": "user", "content": user_input})
    return messages


def chat_loop(args: argparse.Namespace) -> None:
    history = load_history(args.memory)
    embedder = None
    if SentenceTransformer and args.embedding_model:
        embedder = SentenceTransformer(args.embedding_model)
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower().strip() in {"exit", "quit"}:
            break

        context = retrieve_context(user_input, history, embedder, args.top_k)
        messages = build_messages(args.system_prompt, context, user_input)
        payload = {
            "model": args.model,
            "messages": messages,
            "temperature": args.temperature,
        }
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        assistant = resp.json()["choices"][0]["message"]["content"]
        print(f"Assistant: {assistant}\n")

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user_input,
            "assistant": assistant,
        }
        if embedder:
            record["embedding"] = embedder.encode(user_input).tolist()
        history.append(record)
        save_history(args.memory, history)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Simple memory demo with LM Studio")
    p.add_argument("--model", default="lmstudio", help="Model name served by LM Studio")
    p.add_argument("--system-prompt", default="You are a helpful assistant.")
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--memory", default="memory.json", help="Path to JSON memory file")
    p.add_argument("--embedding-model", default="all-MiniLM-L6-v2",
                   help="SentenceTransformer model for embeddings")
    p.add_argument("--top-k", type=int, default=3, help="Number of memories to retrieve")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    chat_loop(args)
