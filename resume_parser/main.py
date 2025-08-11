import pdfplumber
from parser.extractor import extract_entities

def read_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    resume_path = "/home/praveen/Desktop/My-Projects/interview_p/resume_parser/Praveen Resume July 2025 Fullstack.pdf"  # change to your file
    text = read_pdf(resume_path)
    data = extract_entities(text)
    print(data.model_dump_json(indent=2))
