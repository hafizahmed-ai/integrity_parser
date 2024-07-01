import os
from fastapi import HTTPException
from pydantic import BaseModel

class FilePath(BaseModel):
    path: str

def read_text_from_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, "r") as f:
        text = f.read()
    
    return text
