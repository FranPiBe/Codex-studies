"""Generate silly code-inspired poetry."""

import random

WORDS = ["variable", "function", "loop", "module", "class", "syntax"]


def generate_line():
    return f"{random.choice(WORDS).title()} dances with {random.choice(WORDS)}"


def main(lines=5):
    for _ in range(lines):
        print(generate_line())


if __name__ == "__main__":
    main()
