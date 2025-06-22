"""
file_parser.py

This module provides functions to extract text from TXT, DOCX, and PDF files.
You'll learn how to use different libraries for each file type.
"""

import os
from typing import Optional

# For DOCX
import docx
# For PDF
import fitz  # PyMuPDF  # type: ignore


def extract_text_from_txt(file_path: str) -> str:
    """
    Reads a plain text (.txt) file and returns its content as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_text_from_docx(file_path: str) -> str:
    """
    Reads a DOCX file and returns all text as a single string.
    """
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all text as a single string.
    """
    text: list[str] = []  # type hint for better type checking
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text.append(page.get_text())  # type: ignore
    return '\n'.join(text)


def extract_text(file_path: str) -> Optional[str]:
    """
    Detects file type and extracts text using the appropriate function.
    Supported: .txt, .docx, .pdf
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return None

# You can test these functions by calling them with sample file paths.
# Example:
# print(extract_text('sample_resume.pdf'))
# print(extract_text('Cv Harsh.docx'))