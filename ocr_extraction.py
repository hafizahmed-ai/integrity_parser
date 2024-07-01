import pytesseract
from pdf2image import convert_from_path
from fastapi import APIRouter, UploadFile, File
import os
from tempfile import NamedTemporaryFile


router = APIRouter()

# Add poppler to PATH
@router.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    # Read the uploaded file content
    content = await file.read()

    # Save the file content to a temporary file for processing
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    text = ''
    try:
        # Convert PDF pages to images
        pages = convert_from_path(tmp_file_path, 200)

        # Perform OCR on each page
        def process_pages(pages):
            return "\n".join(pytesseract.image_to_string(page) for page in pages)
        
        text = process_pages(pages)
    except Exception as e:
        print(f"Error processing PDF: {e}")  # Print any errors for debugging

    # Save OCR results to a text file in the current directory
    ocr_text_file_path = os.path.join(os.getcwd(), f"{file.filename}.txt")
    with open(ocr_text_file_path, "w") as text_file:
        text_file.write(text)
    
    print(f"OCR results saved at: {ocr_text_file_path}")  # Debugging line

    # Clean up the temporary file
    os.remove(tmp_file_path)

    return {"message": "OCR processing completed", "ocr_text_file_path": ocr_text_file_path}
