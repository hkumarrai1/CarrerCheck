"""
advanced_section_extractor.py

This module uses spaCy to extract key sections (skills, education, experience) from resume text using NLP.
"""
import spacy
from typing import List, Dict

nlp = spacy.load('en_core_web_sm')

# Example skill patterns (expand as needed)
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'machine learning', 'data analysis', 'project management', 'sql', 'excel', 'communication',
    'leadership', 'teamwork', 'problem solving', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'react', 'node', 'django'
]

EDU_ENTITIES = {'ORG', 'GPE', 'DATE', 'PERSON'}


def extract_skills_nlp(text: str) -> List[str]:
    """
    Extracts skills from text using keyword matching and spaCy NER.
    """
    doc = nlp(text)
    found = set()
    for token in doc:
        if token.text.lower() in SKILL_KEYWORDS:
            found.add(token.text)
    # Also look for multi-word skills
    for skill in SKILL_KEYWORDS:
        if skill in text.lower():
            found.add(skill)
    return sorted(found)


def extract_education_nlp(text: str) -> List[str]:
    """
    Extracts education-related entities (ORG, GPE, DATE, PERSON) from text using spaCy NER.
    """
    doc = nlp(text)
    edu = [ent.text for ent in doc.ents if ent.label_ in EDU_ENTITIES]
    return edu


def extract_experience_nlp(text: str) -> List[str]:
    """
    Extracts sentences likely to be experience (containing verbs and dates).
    """
    doc = nlp(text)
    experience = []
    for sent in doc.sents:
        if any(token.pos_ == 'VERB' for token in sent) and any(ent.label_ == 'DATE' for ent in sent.ents):
            experience.append(sent.text.strip())
    return experience

# Example usage:
# skills = extract_skills_nlp(resume_text)
# education = extract_education_nlp(resume_text)
# experience = extract_experience_nlp(resume_text)
