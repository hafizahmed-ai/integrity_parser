Here's a `README.md` file to explain how to run the script, the implementation details, and the features provided:

### README.md


# Insurance Extraction API

This project provides an API to extract specific information from text files, such as dwelling coverage and premium amounts. It uses various techniques including OCR, regex, and Named Entity Recognition (NER) to process the input files.

## Features

- **OCR Extraction**: Convert PDF files to text using OCR (Optical Character Recognition).
- **Regex Extraction**: Extract dwelling coverage and premium amounts from text using regex patterns.
- **NER Extraction**: Use Named Entity Recognition (NER) to extract monetary amounts related to dwelling and premium.
- **NER Extraction with Context**: Enhanced NER to extract monetary amounts with context.

## Setup and Installation

### Prerequisites

- Python 3.6+
- FastAPI
- Uvicorn
- Tesseract OCR
- Poppler-utils

### Installing Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/rizwansaleem01/integrity_parser.git
   cd integrity_parser
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Tesseract OCR and Poppler-utils are installed:
   - **macOS**:
     ```bash
     brew install tesseract
     brew install poppler
     ```
   - **Ubuntu/Linux**:
     ```bash
     sudo apt-get install tesseract-ocr
     sudo apt-get install poppler-utils
     ```
   - **Windows**:
     - Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
     - Download and install [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)

### Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. OCR Extraction

**Endpoint**: `/ocr/extract_text`

**Method**: `POST`

**Description**: Extract text from a PDF file using OCR.

**Request**:
```http
POST /ocr/extract_text
Content-Type: multipart/form-data

file: <PDF file>
```

**Response**:
```json
{
  "text": "<extracted text>"
}
```

### 2. Regex Extraction

**Endpoint**: `/regex/extract_regex`

**Method**: `POST`

**Description**: Extract dwelling coverage and premium amounts from text using regex.

**Request**:
```http
POST /regex/extract_regex
Content-Type: application/json

{
  "path": "/path/to/your/textfile.txt"
}
```

**Response**:
```json
{
  "dwelling_coverage": "<dwelling coverage>",
  "premium_amount": "<premium amount>"
}
```

### 3. NER Extraction

**Endpoint**: `/ner/extract_ner`

**Method**: `POST`

**Description**: Extract monetary amounts related to dwelling and premium using Named Entity Recognition (NER).

**Request**:
```http
POST /ner/extract_ner
Content-Type: application/json

{
  "path": "/path/to/your/textfile.txt"
}
```

**Response**:
```json
{
  "dwelling_feat": "<dwelling feature>",
  "premium_feat": "<premium feature>"
}
```

### 4. NER Extraction with Context

**Endpoint**: `/ner_money/extract_ner_money`

**Method**: `POST`

**Description**: Enhanced NER to extract monetary amounts related to dwelling and premium with context.

**Request**:
```http
POST /ner_money/extract_ner_money
Content-Type: application/json

{
  "path": "/path/to/your/textfile.txt"
}
```

**Response**:
```json
{
  "dwelling_feat": "<dwelling feature>",
  "premium_feat": "<premium feature>"
}
```

## Implementation Details

### Project Structure

- **main.py**: Main entry point for the FastAPI application, including the router setup.
- **ocr_extraction.py**: Contains the endpoint for extracting text from PDF files using OCR.
- **regex_extraction.py**: Contains the endpoint for extracting information using regex patterns.
- **ner_extraction.py**: Contains the endpoint for extracting information using Named Entity Recognition (NER) where custom matching patterns has been used for extraction of required features.
- **ner_extraction_money.py**: Contains the enhanced NER endpoint for extracting monetary amounts with context for extracting features by applying rules using the context around them.
- **utils.py**: Contains shared utilities, such as the `FilePath` model and the `read_text_from_file` function.

### Centralized Utilities

- **FilePath Model**: Represents the file path input.
- **read_text_from_file Function**: Reads text from a given file path, raising an HTTP 404 exception if the file is not found.

### Example Request

Here's an example of how to send a request to one of the endpoints using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/regex/extract_regex" -H "Content-Type: application/json" -d '{"path": "/path/to/your/textfile.txt"}'
```



### Explanation

1. **Project Features**: Lists the main features provided by the API, such as OCR extraction, regex extraction, and NER extraction.
2. **Setup and Installation**: Provides step-by-step instructions to set up the environment, install dependencies, and run the server.
3. **API Endpoints**: Details the available API endpoints, including their methods, descriptions, request formats, and example responses.
4. **Implementation Details**: Describes the project structure and centralized utilities, explaining how different parts of the project are organized and how they interact.
