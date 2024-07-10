import spacy
from spacy.matcher import Matcher
import re
from fastapi import APIRouter
from utils import FilePath, read_text_from_file

router = APIRouter()

# Ensure the model is downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    cleaned_text = re.sub(r"[-=]+", " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text

@router.post("/extract_ner")
async def extract_ner(file_path: FilePath):
    ner_text = read_text_from_file(file_path.path)
    matcher = Matcher(nlp.vocab)

    # Define updated patterns
    pattern_dwelling = [
        {"LOWER": {"IN": ["dwelling", "dwlg", "dwelling."]}},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_ASCII": True, "OP": "*", "IS_PUNCT": False, "IS_SPACE": False},
        {"TEXT": {"REGEX": r"^\$?\d[\d,]*\.?\d*$"}}
    ]

    pattern_premium = [
        {"LOWER": {"IN": ["total", "annual", "total.", "annual."]}},
        {"LOWER": "premium"},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_ASCII": True, "OP": "*", "IS_PUNCT": False, "IS_SPACE": False},
        {"TEXT": {"REGEX": r"^\$?\d[\d,]*\.?\d*$"}}
    ]

    dwelling_feat = []
    premium_feat = []

    doc = nlp(clean_text(ner_text))

    matcher.add("DWELLING_PATTERN", [pattern_dwelling])
    matcher.add("PREMIUM_PATTERN", [pattern_premium])

    matches = matcher(doc)

    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings["DWELLING_PATTERN"]:
            dwell_amt = extract_numeric_value(doc, start, end, exclude_keywords=["premium"])
            if dwell_amt:
                dwelling_feat.append(dwell_amt)

        elif match_id == nlp.vocab.strings["PREMIUM_PATTERN"]:
            prem_amt = extract_numeric_value(doc, start, end, exclude_keywords=["dwelling"])
            if prem_amt:
                premium_feat.append(prem_amt)


    max_dwelling = max(dwelling_feat, key=float) if dwelling_feat else None
    max_premium = max(premium_feat, key=float) if premium_feat else None

    return {
        "dwelling_feat": max_dwelling,
        "premium_feat": max_premium
    }

def extract_numeric_value(doc, start, end, exclude_keywords=[]):
    span_text = doc[start:end].text.lower()
    if any(keyword in span_text for keyword in exclude_keywords):
        return None
    for token in doc[start:end]:
        if token.text.startswith('$') and token.like_num:
            return token.text[1:].replace(',', '')  # Remove '$' and replace commas
        elif token.like_num:
            return token.text.replace(',', '')
    return None
