import re
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
import logging

MAX_CHUNKS = 512

def chunk_pdf(content: bytes, chunk_size: int = 500, overlap: int = 100, use_ocr: bool = True) -> List[str]:
    def extract_text(pdf_bytes: bytes, ocr_enabled: bool = True) -> str:
        try:
            reader = PdfReader(BytesIO(pdf_bytes))
            text_pages = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    cleaned = re.sub(r'\s+', ' ', page_text)
                    text_pages.append(cleaned.strip())
            if text_pages:
                return "\n\n".join(text_pages)

            # Fallback to OCR only if enabled and no text extracted
            if ocr_enabled:
                images = convert_from_bytes(pdf_bytes)
                ocr_texts = [pytesseract.image_to_string(img, lang='eng') for img in images]
                return "\n\n".join(ocr_texts)
            else:
                return ""

        except Exception as e:
            raise ValueError(f"Could not extract text from PDF: {str(e)}")

    text = extract_text(content, ocr_enabled=use_ocr)
    if not text:
        raise ValueError("No text extracted from PDF.")

    paragraphs = re.split(r'(?<=[.!?])\s+|\n{2,}', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current = []
    total_len = 0
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        if total_len + len(para) <= chunk_size:
            current.append(para)
            total_len += len(para)
            i += 1
        else:
            chunks.append(" ".join(current))
            # handle overlap
            j = len(current) - 1
            overlap_paragraphs = []
            overlap_len = 0
            while j >= 0 and overlap_len < overlap:
                overlap_paragraphs.insert(0, current[j])
                overlap_len += len(current[j])
                j -= 1
            current = overlap_paragraphs
            total_len = sum(len(p) for p in current)

        if len(chunks) >= MAX_CHUNKS:
            logging.warning(f"Reached max chunks limit: {MAX_CHUNKS}. Stopping further chunking.")
            break

    if current and len(chunks) < MAX_CHUNKS:
        chunks.append(" ".join(current))

    logging.info(f"Extracted {len(chunks)} chunks from PDF")
    return chunks
