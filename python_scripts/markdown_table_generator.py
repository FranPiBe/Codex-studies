"""Markdown Table Generator
-------------------------
Convert a CSV file into a Markdown-formatted table.

Example::
    python markdown_table_generator.py data.csv -d ';' -o table.md
"""

import argparse
import csv
import os
from typing import List


def escape_pipe(text: str) -> str:
    """Escape pipe characters used in Markdown tables."""
    return text.replace("|", "\\|")


def read_csv(path: str, delimiter: str) -> List[List[str]]:
    """Return rows from CSV file as list of lists."""
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f, delimiter=delimiter)]


def to_markdown(rows: List[List[str]]) -> str:
    """Convert rows to a Markdown table string."""
    if not rows:
        return ""
    header, *body = rows
    header = [escape_pipe(cell) for cell in header]
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("|" + "|".join([" --- " for _ in header]) + "|")
    for row in body:
        row = [escape_pipe(cell) for cell in row]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def write_output(text: str, path: str = None) -> None:
    """Write Markdown to *path* or print to stdout."""
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Wrote {path}")
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown table from CSV")
    parser.add_argument("csvfile", help="Path to CSV file")
    parser.add_argument("-d", "--delimiter", default=",", help="CSV delimiter")
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    args = parser.parse_args()

    if not os.path.isfile(args.csvfile):
        parser.error(f"{args.csvfile} is not a file")
    rows = read_csv(args.csvfile, args.delimiter)
    markdown = to_markdown(rows)
    write_output(markdown, args.output)


if __name__ == "__main__":
    main()
