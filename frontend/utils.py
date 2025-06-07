import requests
from config import UPLOAD_ENDPOINT, QUERY_ENDPOINT

def upload_pdf(file):
    files = {"file": file}
    response = requests.post(UPLOAD_ENDPOINT, files=files)
    return response.json()

def query_llm(question):
    data = {"question": question}
    response = requests.post(QUERY_ENDPOINT, json=data)
    return response.json()
