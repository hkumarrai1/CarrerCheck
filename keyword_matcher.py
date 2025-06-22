"""
keyword_matcher.py

This module provides functions to extract keywords from text, calculate overlap, and score the match between resume and job description.
You'll learn about NLP basics, tokenization, and set operations.
"""

import spacy
from typing import Set, Tuple

# Load spaCy English model (make sure to run: python -m spacy download en_core_web_sm)
nlp = spacy.load('en_core_web_sm')

def extract_keywords(text: str) -> Set[str]:
    """
    Extracts keywords (nouns, proper nouns, and verbs) from the text using spaCy.
    Returns a set of unique keywords (lowercased).
    """
    doc = nlp(text)
    keywords: Set[str] = set()
    for token in doc:
        if token.pos_ in {'NOUN', 'PROPN', 'VERB'} and not token.is_stop and token.is_alpha:
            keywords.add(token.lemma_.lower())
    return keywords


def calculate_overlap(resume_keywords: Set[str], jd_keywords: Set[str]) -> Tuple[int, int, float, Set[str]]:
    """
    Calculates the overlap between resume and job description keywords.
    Returns (num_matched, total_jd_keywords, match_score, missing_keywords)
    """
    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    score = len(matched) / len(jd_keywords) if jd_keywords else 0.0
    return len(matched), len(jd_keywords), score, missing

# Example usage:
# from file_parser import extract_text
# from section_extractor import extract_skills
# from keyword_matcher import extract_keywords, calculate_overlap
# resume_text = extract_text('Cv Harsh.docx')
# jd_text = extract_text('job_description.txt')
# resume_keywords = extract_keywords(resume_text)
# jd_keywords = extract_keywords(jd_text)
# num_matched, total_jd, score, missing = calculate_overlap(resume_keywords, jd_keywords)
# print(f"Match score: {score*100:.1f}%")
# print(f"Missing keywords: {missing}")
