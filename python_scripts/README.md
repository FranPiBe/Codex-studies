# Python Scripts

This folder contains small, standalone scripts demonstrating useful patterns in Python.
Each script can be run directly from the command line and is written to be easy
to read, reuse, or extend.

## Available Scripts

- **hello_codex.py** – simple example showing `argparse` and file output.
  ```bash
  python hello_codex.py YourName -o greeting.txt
  ```
- **file_organizer.py** – organize files into subfolders based on extension.
  ```bash
  python file_organizer.py /path/to/downloads --dry-run
  ```
- **pdf_to_text.py** – extract text from all PDFs in a folder using `PyPDF2`.
  ```bash
  python pdf_to_text.py ./pdfs -o texts
  ```
- **log_parser.py** – count ERROR/WARNING/INFO entries in a log file.
  ```bash
  python log_parser.py system.log --csv summary.csv
  ```
- **markdown_table_generator.py** – convert a CSV file to a Markdown table.
  ```bash
  python markdown_table_generator.py data.csv -o table.md
  ```

## Dependencies

Only `pdf_to_text.py` requires an external dependency:

- `PyPDF2` – install with `pip install PyPDF2`

All other scripts rely solely on Python's standard library.
