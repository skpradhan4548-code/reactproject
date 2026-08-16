from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import io

app = FastAPI(title="DocuAgent API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Read the uploaded file into memory
    contents = await file.read()
    
    # PdfReader needs a file-like object, not raw bytes — io.BytesIO wraps the bytes
    pdf_stream = io.BytesIO(contents)
    reader = PdfReader(pdf_stream)
    
    # Extract text from every page and join it together
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    
    return {
        "filename": file.filename,
        "num_pages": len(reader.pages),
        "text_preview": full_text[:500],  # just first 500 chars so the response isn't huge
        "total_chars": len(full_text)
    }