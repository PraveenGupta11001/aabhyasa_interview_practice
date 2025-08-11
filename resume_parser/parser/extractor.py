import spacy
from .utils import extract_email, extract_phone
from pydantic import BaseModel
from typing import List, Optional

# Load spaCy model globally (fastest)
nlp = spacy.load("en_core_web_sm")

class ResumeData(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]

def extract_entities(text: str) -> ResumeData:
    doc = nlp(text)

    name = None
    skills = []
    education = []
    experience = []

    # Named Entity Recognition
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ in ["ORG", "GPE"]:
            education.append(ent.text)
        elif ent.label_ in ["WORK_OF_ART", "PRODUCT"]:
            skills.append(ent.text)

    # Keyword-based skill extraction (simple demo)
    common_skills = ["Python", "Java", "SQL", "Machine Learning", "Django", "React"]
    for token in doc:
        if token.text in common_skills:
            skills.append(token.text)

    # Regex for email & phone
    email = extract_email(text)
    phone = extract_phone(text)

    return ResumeData(
        name=name,
        email=email,
        phone=phone,
        skills=list(set(skills)),
        education=list(set(education)),
        experience=list(set(experience))
    )
