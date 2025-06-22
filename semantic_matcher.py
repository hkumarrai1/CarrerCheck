"""
semantic_matcher.py

This module provides functions to compute semantic similarity between resume and job description using sentence embeddings.
You'll learn about embeddings, cosine similarity, and how to use sentence-transformers.
"""

from sentence_transformers import SentenceTransformer, util

# Load a pre-trained sentence transformer model (offline, open-source)
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between two texts using sentence embeddings.
    Returns a similarity score between 0 and 1.
    """
    emb1 = model.encode(text1, convert_to_tensor=True)  # type: ignore
    emb2 = model.encode(text2, convert_to_tensor=True)  # type: ignore
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    return similarity

# Example usage:
# from file_parser import extract_text
# from semantic_matcher import compute_semantic_similarity
# resume_text = extract_text('Cv Harsh.docx')
# jd_text = extract_text('job_description.txt')
# score = compute_semantic_similarity(resume_text, jd_text)
# print(f"Semantic similarity score: {score:.2f}")
