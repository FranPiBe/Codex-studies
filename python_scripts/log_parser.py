"""Log Parser
-----------
Summarize log levels (ERROR, WARNING, INFO) in a log file. Optionally group by
date if the log begins with a ``YYYY-MM-DD`` timestamp.

Usage::
    python log_parser.py path/to/logfile [--csv summary.csv]
"""

import argparse
import csv
import os
import re
from collections import defaultdict
from typing import Dict, Iterable

LEVELS = ("ERROR", "WARNING", "INFO")


def parse_lines(lines: Iterable[str]) -> Dict[str, Dict[str, int]]:
    """Return counts of levels by date.

    If no date is found in a line, all counts are stored under ``"all"``.
    """
    totals: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    date_re = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})")
    level_re = re.compile(r"\b(ERROR|WARNING|INFO)\b")

    for line in lines:
        date_match = date_re.match(line)
        date = date_match.group("date") if date_match else "all"
        level_match = level_re.search(line)
        if level_match:
            level = level_match.group(1)
            totals[date][level] += 1
    return totals


def print_summary(stats: Dict[str, Dict[str, int]]) -> None:
    """Print a formatted summary to stdout."""
    for date, counts in sorted(stats.items()):
        summary = ", ".join(f"{lvl}: {counts.get(lvl,0)}" for lvl in LEVELS)
        print(f"{date} -> {summary}")


def write_csv(stats: Dict[str, Dict[str, int]], csv_path: str) -> None:
    """Write summary statistics to ``csv_path``."""
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", *LEVELS])
        for date, counts in sorted(stats.items()):
            row = [date] + [counts.get(lvl, 0) for lvl in LEVELS]
            writer.writerow(row)
    print(f"Wrote {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse log file for level counts")
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--csv", help="Optional output CSV path")
    args = parser.parse_args()

    if not os.path.isfile(args.logfile):
        parser.error(f"{args.logfile} is not a file")
    with open(args.logfile, "r", encoding="utf-8", errors="ignore") as f:
        stats = parse_lines(f)

    if args.csv:
        write_csv(stats, args.csv)
    else:
        print_summary(stats)


if __name__ == "__main__":
    main()
