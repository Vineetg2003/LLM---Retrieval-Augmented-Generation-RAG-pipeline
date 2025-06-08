import re
from typing import List
from io import BytesIO
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
import logging

def chunk_pdf(content: bytes, chunks_per_page: int = 5, overlap_ratio: float = 0.2, use_ocr: bool = True) -> List[str]:
    def extract_text_per_page(pdf_bytes: bytes, ocr_enabled: bool = True) -> List[str]:
        try:
            reader = PdfReader(BytesIO(pdf_bytes))
            pages_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    cleaned = re.sub(r'\s+', ' ', page_text).strip()
                    pages_text.append(cleaned)
                else:
                    pages_text.append("")  # empty page
            # OCR fallback if all pages empty
            if all(not p for p in pages_text) and ocr_enabled:
                images = convert_from_bytes(pdf_bytes)
                pages_text = [pytesseract.image_to_string(img, lang='eng').strip() for img in images]
            return pages_text
        except Exception as e:
            raise ValueError(f"[chunker] Text extraction failed: {e}")

    def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
        words = text.split()
        if len(words) <= chunk_size:
            return [text]
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    pages_text = extract_text_per_page(content, ocr_enabled=use_ocr)
    all_chunks = []

    for page_num, page_text in enumerate(pages_text, start=1):
        if not page_text:
            continue
        words_count = len(page_text.split())
        chunk_size = max(50, words_count // chunks_per_page)  # minimum chunk size 50 words
        overlap = int(chunk_size * overlap_ratio)
        page_chunks = chunk_text(page_text, chunk_size=chunk_size, overlap=overlap)
        logging.info(f"[chunker] Page {page_num} split into {len(page_chunks)} chunks (chunk_size={chunk_size}, overlap={overlap})")
        all_chunks.extend(page_chunks)

    logging.info(f"[chunker] Total chunks extracted: {len(all_chunks)}")
    return all_chunks
