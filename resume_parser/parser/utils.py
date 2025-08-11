import re

def extract_email(text: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text: str):
    match = re.search(r'\+?\d[\d\s\-\(\)]{7,}\d', text)
    return match.group(0) if match else None
