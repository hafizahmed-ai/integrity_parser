import re
from fastapi import APIRouter
from utils import FilePath, read_text_from_file

router = APIRouter()

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

@router.post("/extract_regex")
async def extract_regex(file_path: FilePath):
    text = read_text_from_file(file_path.path)

    match_dwelling = re.search(regex_pattern_dwelling, text, re.IGNORECASE | re.VERBOSE)
    match_premium = re.search(regex_pattern_final_premium, text, re.IGNORECASE | re.VERBOSE)

    dwelling_coverage = match_dwelling.group(1).replace(',', '').rstrip('.') if match_dwelling else None
    premium_amount = match_premium.group(1).replace(',', '').rstrip('.') if match_premium else None

    return {"dwelling_coverage": dwelling_coverage, "premium_amount": premium_amount}
