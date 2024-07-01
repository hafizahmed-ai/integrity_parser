import spacy
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

regex_pattern_dwelling = r"""
    (?:Dwelling|dwlg|DWELLING)         # Match variations of "Dwelling"
    .*?                                # Match any characters (non-greedy)
    \$?                                # Optional "$" symbol
    (\d[\d,.]*)                        # Capture numeric value
    """

regex_pattern_final_premium = r"""
    (?:total\sannual\spremium|total\spremium|annual\spremium)  # Match variations of "total annual premium" or "total premium"
    .*?                                        # Match any characters (non-greedy)
    \$?                                        # Optional "$" symbol
    (\d[\d,.]*)                                # Capture numeric value
    """

def clean_text(text):
    cleaned_text = re.sub(r"[-=]+", " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text

@router.post("/extract_ner_money")
async def extract_ner_money(file_path: FilePath):
    text = read_text_from_file(file_path.path)

    doc = nlp(clean_text(text))
    dwelling_feat = []
    premium_feat = []

    for ent in doc.ents:
        if ent.label_ == 'MONEY':
            value = ent.text

            # get left words
            left_words = []
            for i in range(max(ent.start - 10, 0), ent.start):
                left_words.append(doc[i].text)

            # get right words
            right_words = []
            for i in range(ent.end, min(ent.end + 10, len(doc))):
                right_words.append(doc[i].text)

            context = " ".join(left_words + [value] + right_words)

            match_dwelling = re.search(regex_pattern_dwelling, context, re.IGNORECASE | re.VERBOSE)

            if match_dwelling:
                dwell_amt = match_dwelling.group(1).replace(',', '')
                dwelling_feat.append(float(dwell_amt))

            match_premium = re.search(regex_pattern_final_premium, context, re.IGNORECASE | re.VERBOSE)
            if match_premium:
                prem_amt = match_premium.group(1).replace(',', '')
                premium_feat.append(float(prem_amt))

    max_dwelling = max(dwelling_feat, key=float) if dwelling_feat else None
    max_premium = max(premium_feat, key=float) if premium_feat else None

    return {"dwelling_feat": max_dwelling, "premium_feat": max_premium}
