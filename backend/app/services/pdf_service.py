import io
import PyPDF2

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts text from a given PDF byte array using PyPDF2.
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text_content = []
    
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text_content.append(extracted)
            
    return "\n".join(text_content)
