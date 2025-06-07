from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO

def test_pdf_extraction(path):
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if text.strip():
            print("Native extraction success:")
            print(text[:500])  # print first 500 chars
            return
        print("Native extraction failed, trying OCR...")

        images = convert_from_bytes(pdf_bytes)
        ocr_texts = []
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            print(f"OCR page {i+1} length: {len(text)}")
            ocr_texts.append(text)

        combined_text = "\n".join(ocr_texts)
        if combined_text.strip():
            print("OCR extraction success:")
            print(combined_text[:500])
        else:
            print("OCR extraction failed: No text found.")
    except Exception as e:
        print(f"Extraction failed: {e}")


if __name__ == "__main__":
    import sys
    test_pdf_extraction(sys.argv[1])
