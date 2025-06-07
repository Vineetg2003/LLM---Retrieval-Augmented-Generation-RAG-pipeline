import hashlib
import re

def get_file_hash(content: bytes) -> str:
    """Generate SHA256 hash for duplicate detection"""
    return hashlib.sha256(content).hexdigest()

def validate_pdf(content: bytes) -> bool:
    """Basic PDF validation"""
    return content.startswith(b'%PDF-') and content.endswith(b'%%EOF\n')
