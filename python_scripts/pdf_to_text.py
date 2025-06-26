"""PDF to Text Converter
-----------------------
Extract text content from all PDF files in a folder.

Requires ``PyPDF2``. Example::
    python pdf_to_text.py /path/to/pdfs -o output_folder
"""

import argparse
import os
from pathlib import Path
from typing import Iterable

from PyPDF2 import PdfReader


def pdf_files(directory: str) -> Iterable[Path]:
    """Yield ``Path`` objects for PDF files inside *directory*."""
    for entry in Path(directory).iterdir():
        if entry.is_file() and entry.suffix.lower() == ".pdf":
            yield entry


def extract_text(pdf_path: Path) -> str:
    """Return the full text from a PDF file."""
    try:
        reader = PdfReader(str(pdf_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:  # catch parsing errors
        raise RuntimeError(f"Failed to read {pdf_path}: {exc}")


def convert_all(src_dir: str, out_dir: str) -> None:
    """Write text versions of all PDFs in ``src_dir`` to ``out_dir``."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for pdf in pdf_files(src_dir):
        txt_path = Path(out_dir) / (pdf.stem + ".txt")
        try:
            text = extract_text(pdf)
        except Exception as e:
            print(e)
            continue
        txt_path.write_text(text, encoding="utf-8")
        print(f"Wrote {txt_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from PDFs")
    parser.add_argument("src", help="Folder containing PDF files")
    parser.add_argument("-o", "--output", default="texts", help="Output folder")
    args = parser.parse_args()

    if not os.path.isdir(args.src):
        parser.error(f"{args.src} is not a directory")
    convert_all(args.src, args.output)


if __name__ == "__main__":
    main()
