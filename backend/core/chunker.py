import re
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract

def chunk_pdf(content: bytes, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    def extract_text(pdf_bytes: bytes) -> str:
        try:
            reader = PdfReader(BytesIO(pdf_bytes))
            text_pages = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    cleaned = re.sub(r'\n(?=[^\n])', ' ', page_text)
                    text_pages.append(cleaned.strip())
            text = "\n\n".join(text_pages).strip()
            if text:
                return text

            # Fallback to OCR
            images = convert_from_bytes(pdf_bytes)
            ocr_texts = [pytesseract.image_to_string(img) for img in images]
            return "\n\n".join(ocr_texts)

        except Exception as e:
            raise ValueError(f"Could not extract text from PDF: {str(e)}")

    text = extract_text(content)
    paragraphs = [p.strip() for p in re.split(r'\n{2,}|\.\s+', text) if p.strip()]
    
    chunks = []
    current_chunk = ""
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
            i += 1
        else:
            chunks.append(current_chunk.strip())
            # create overlap from end of current_chunk
            overlap_chunk = ""
            j = i - 1
            while j >= 0 and len(overlap_chunk) + len(paragraphs[j]) + 2 <= overlap:
                overlap_chunk = paragraphs[j] + ("\n\n" if overlap_chunk else "") + overlap_chunk
                j -= 1
            current_chunk = overlap_chunk

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
