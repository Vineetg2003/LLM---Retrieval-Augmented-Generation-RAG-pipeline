def test_chunking():
    from core.chunker import chunk_pdf
    content = b"Dummy PDF text for test" * 100
    chunks = chunk_pdf(content)
    assert len(chunks) > 0

def test_query_response():
    from core.llm import generate_answer
    result = generate_answer("What is this?", "This is a test context.")
    assert isinstance(result, str)
