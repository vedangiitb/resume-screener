import pdfplumber
import requests
from io import BytesIO
from .get_resume_url import get_resume_url

def extract_text(link,url,key):
    pdf_url = get_resume_url(link,url,key)
    if (pdf_url):
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return []
        
        file_like = BytesIO(response.content)

        all_lines = []
        with pdfplumber.open(file_like) as pdf:
            for page in pdf.pages:
                text = page.extract_text(layout=True,x_tolerance=1.5, y_tolerance=1)
                if text:
                    lines = text.split("\n")
                    cleaned_line = [line.strip() for line in lines]
                    all_lines.extend(cleaned_line)
        return all_lines
    else:
        print("Error while getting URL")
