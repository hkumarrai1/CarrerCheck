from file_parser import extract_text
# from section_extractor import extract_skills
from keyword_matcher import extract_keywords, calculate_overlap
from semantic_matcher import compute_semantic_similarity
import difflib



resume_text = extract_text('Cv Harsh.docx')
jd_text = extract_text('job_description.txt')

def suggest_similar_keywords(missing: set[str], resume_keywords: set[str]) -> dict[str, list[str]]:
    """
    For each missing keyword, suggest similar words already present in the resume (fuzzy match).
    """
    suggestions: dict[str, list[str]] = {}
    for kw in missing:
        close = difflib.get_close_matches(kw, resume_keywords, n=2, cutoff=0.7)
        if close:
            suggestions[kw] = close
    return suggestions

if resume_text is not None and jd_text is not None:
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    num_matched, total_jd, score, missing = calculate_overlap(resume_keywords, jd_keywords)
    print(f"Match score: {score*100:.1f}%")
    print(f"Missing keywords: {missing}")
    if missing:
        print("\nSuggestions to improve your resume:")
        print("- Add these missing keywords/skills from the job description:")
        for kw in sorted(missing):
            print(f"  - {kw}")
        # Advanced: Suggest similar words already present
        similar = suggest_similar_keywords(missing, resume_keywords)
        if similar:
            print("\nYou have similar words in your resume for some missing keywords:")
            for kw, matches in similar.items():
                print(f"  - {kw}: similar in your resume -> {', '.join(matches)}")
    semantic_score = compute_semantic_similarity(resume_text, jd_text)
    print(f"\nSemantic similarity score: {semantic_score:.2f}")
else:
    if resume_text is None:
        print("Could not extract text from the resume file.")
    if jd_text is None:
        print("Could not extract text from the job description file.")