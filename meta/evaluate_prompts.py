import os
import textwrap
from typing import List, Tuple

# Optional dependency; script can run offline with a mocked response
try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - environment may not have openai
    openai = None  # type: ignore

TASK_DESCRIPTION = (
    "Generate Python code defining a function `parse_and_average` "
    "that takes a CSV string with headers and returns a dictionary "
    "of column averages."
)

BASE_DIR = os.path.dirname(__file__)
PROMPTS_FILE = os.path.join(BASE_DIR, "prompts.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "results")
NUM_TOP = 3

def call_codex(prompt: str, task: str) -> str:
    """Query OpenAI Codex (or return a mocked response if unavailable)."""
    if openai and os.getenv("OPENAI_API_KEY"):
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": task},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )
            return completion.choices[0].message.content.strip()
        except Exception:
            pass
    return mock_codex_response(prompt, task)

def mock_codex_response(prompt: str, task: str) -> str:
    """Return a simple hard-coded implementation used when offline."""
    code = """
def parse_and_average(csv_text):
    import csv
    from io import StringIO
    reader = csv.DictReader(StringIO(csv_text))
    sums = {}
    count = 0
    for row in reader:
        for k, v in row.items():
            sums[k] = sums.get(k, 0.0) + float(v)
        count += 1
    return {k: v / count for k, v in sums.items()}
"""
    return textwrap.dedent(code).strip()

def evaluate_code(code: str) -> Tuple[int, str]:
    """Score the generated code and return (score, summary)."""
    score = 0
    summary_parts: List[str] = []

    try:
        compiled = compile(code, "<generated>", "exec")
        score += 1
        summary_parts.append("compiled")
    except SyntaxError as exc:
        summary_parts.append(f"syntax error: {exc}")
        return score, "; ".join(summary_parts)

    local_env: dict = {}
    try:
        exec(compiled, local_env)
        func = local_env.get("parse_and_average")
        if not callable(func):
            summary_parts.append("parse_and_average missing")
            return score, "; ".join(summary_parts)

        csv_text = "A,B\n1,2\n3,4\n"
        expected = {"A": 2.0, "B": 3.0}
        if func(csv_text) == expected:
            score += 2
            summary_parts.append("function works")
        else:
            summary_parts.append("incorrect result")
    except Exception as exc:  # pragma: no cover - evaluation runtime errors
        summary_parts.append(f"runtime error: {exc}")

    lines = [ln for ln in code.splitlines() if ln.strip()]
    if len(lines) <= 20:
        score += 1
        summary_parts.append("concise")
    else:
        summary_parts.append("too long")

    return score, "; ".join(summary_parts)

def load_prompts(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_markdown(path: str, prompt: str, response: str, score: int, summary: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Best Prompt\n\n")
        f.write("## Prompt\n")
        f.write("```")
        f.write(f"\n{prompt}\n")
        f.write("```\n\n")
        f.write("## Codex Response\n")
        f.write("```python\n")
        f.write(response)
        f.write("\n```\n\n")
        f.write(f"**Score:** {score}  \n")
        f.write(f"**Evaluation:** {summary}\n")

def main() -> None:
    prompts = load_prompts(PROMPTS_FILE)
    results = []

    for prompt in prompts:
        response = call_codex(prompt, TASK_DESCRIPTION)
        score, summary = evaluate_code(response)
        results.append({
            "prompt": prompt,
            "response": response,
            "score": score,
            "summary": summary,
        })

    results.sort(key=lambda r: r["score"], reverse=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    top_n = min(NUM_TOP, len(results))
    for idx in range(top_n):
        r = results[idx]
        save_markdown(
            os.path.join(OUTPUT_DIR, f"best_prompt_{idx + 1}.md"),
            r["prompt"],
            r["response"],
            r["score"],
            r["summary"],
        )

    leaderboard = os.path.join(OUTPUT_DIR, "prompt_leaderboard.md")
    with open(leaderboard, "w", encoding="utf-8") as f:
        f.write("# Prompt Leaderboard\n\n")
        f.write("| Rank | Score | Prompt |\n")
        f.write("|-----:|-----:|-------|\n")
        for idx, r in enumerate(results, 1):
            snippet = r["prompt"].replace("|", "\\|")
            if len(snippet) > 50:
                snippet = snippet[:47] + "..."
            f.write(f"| {idx} | {r['score']} | {snippet} |\n")
    print(f"Results written to '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()
