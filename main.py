from fastapi import FastAPI
from ocr_extraction import router as ocr_router
from regex_extraction import router as regex_router
from ner_extraction import router as ner_router
from ner_extraction_otherlogic import router as ner_money_router

app = FastAPI()

app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(regex_router, prefix="/regex", tags=["Regex"])
app.include_router(ner_router, prefix="/ner", tags=["NER"])
app.include_router(ner_money_router, prefix="/ner_money", tags=["NER Money"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Insurance Extraction API!"}
