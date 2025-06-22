"""
section_extractor.py

This module provides functions to extract key sections (Skills, Education, Experience, Keywords) from resume or job description text.
You'll learn how to use regex and text processing for section extraction.
"""

import re
from typing import Optional, Dict


SECTION_HEADERS = [
    'skills',
    'education',
    'experience',
    'work experience',
    'professional experience',
    'projects',
    'certifications',
    'summary',
    'objective',
    'achievements',
    'keywords',
]


def split_into_sections(text: str) -> Dict[str, str]:
    """
    Splits the text into sections based on common resume/job description headers.
    Returns a dictionary: {section_name: section_text}
    """
    # Build a regex pattern to match section headers
    pattern = r'(^|\n)\s*(' + '|'.join([re.escape(h) for h in SECTION_HEADERS]) + r')\s*[:\-]?\s*(?=\n|$)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
    sections: Dict[str, str] = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        header = match.group(2).strip().lower()
        sections[header] = text[start:end].strip()
    return sections


def extract_section(text: str, section: str) -> Optional[str]:
    """
    Extracts a specific section by name (e.g., 'skills') from the text.
    Returns the section text or None if not found.
    """
    sections = split_into_sections(text)
    return sections.get(section.lower())


def extract_skills(text: str) -> Optional[str]:
    """
    Extracts the 'skills' section from the text.
    """
    return extract_section(text, 'skills')


def extract_education(text: str) -> Optional[str]:
    """
    Extracts the 'education' section from the text.
    """
    return extract_section(text, 'education')


def extract_experience(text: str) -> Optional[str]:
    """
    Extracts the 'experience' section from the text.
    """
    # Try both 'experience' and 'work experience'
    exp = extract_section(text, 'experience')
    if exp:
        return exp
    return extract_section(text, 'work experience')

# You can test these functions by passing the output of extract_text() from file_parser.py
# Example:
# from file_parser import extract_text
# text = extract_text('Cv Harsh.docx')
# from section_extractor import extract_skills, extract_education, extract_experience
# print(extract_skills(text))
# print(extract_education(text))
# print(extract_experience(text))




# text = extract_text('Cv Harsh.docx')
# if text is not None:
#     print(extract_skills(text))
#     print(extract_education(text))
#     print(extract_experience(text))
# else:
#     print("Could not extract text from the file.")
