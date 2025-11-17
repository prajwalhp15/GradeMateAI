import re
from difflib import SequenceMatcher

def normalize_code(code: str) -> str:
    # Remove triple-double docstrings and comments, whitespace normalize
    code = re.sub(r'(?s)"""(.*?)"""', '', code)
    code = re.sub(r'#.*', '', code)
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    norm = " ".join(lines)
    norm = re.sub(r'\s+', ' ', norm)
    return norm.lower()

def similarity(a: str, b: str) -> float:
    an = normalize_code(a)
    bn = normalize_code(b)
    if not an or not bn:
        return 0.0
    ratio = SequenceMatcher(None, an, bn).ratio()
    return ratio * 100.0

def is_plagiarized(score_percent: float, threshold: float = 91.0) -> bool:
    return score_percent >= threshold
