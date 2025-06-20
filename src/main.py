import modal
from fastapi import Request
from .extract_text import extract_text
from .preprocess_text import preprocess_text
from .classify_job_text import classify_job_text
import os
import re

app = modal.App("resume-screener")

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi[standard]", "pdfplumber", "supabase", "sentence-transformers", "joblib",  "requests")
    .env({
        "MODEL_PATH": "/root/embedding_model",
        "CLF_PATH": "/root/valid_point_classifier.pkl",
        "LABEL_PATH":"/root/label_encoder.pkl"
    })
    .add_local_dir("embedding_model", "/root/embedding_model")
    .add_local_file("valid_point_classifier.pkl", "/root/valid_point_classifier.pkl")
    .add_local_file("label_encoder.pkl", "/root/label_encoder.pkl")
)


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("supabase-secrets")],
)
@modal.fastapi_endpoint(method="POST")
async def main(request: Request):
    try:
        body = await request.json()
        job_text = body.get("job_text", "")
        resume_url = body.get("resume_link", "")
        if not job_text or not resume_url:
            return {"status": 400, "message": "Missing job text or resume text"}
        url = os.environ["PUBLIC_SUPABASE_URL"]
        key = os.environ["PUBLIC_SUPABASE_ANON_KEY"]
        resume_points = preprocess_text(extract_text(resume_url, url, key))
        job_points = preprocess_text(re.split(r'\.\s+|\n',job_text))
        tech_points = [] 
        edu_points = []
        invalid_points = []
        for point in job_points:
            if classify_job_text(point)==2:
                edu_points.append(point)
            elif classify_job_text(point)==1:
                tech_points.append(point)
            else:
                invalid_points.append(point)

        print("Educational Points")
        print(edu_points)

        print("Tech points")
        print(tech_points)

        print("Invalid Points")
        print(invalid_points)

        tech_skill_points = [] 
        edu_skill_points = []
        invalid_skill_points = []
        for point in resume_points:
            if classify_job_text(point)==2:
                edu_skill_points.append(point)
            elif classify_job_text(point)==1:
                tech_skill_points.append(point)
            else:
                invalid_skill_points.append(point)

        print("Educational Points")
        print(edu_skill_points)

        print("Tech points")
        print(tech_skill_points)

        print("Invalid Points")
        print(invalid_skill_points)

        return {"status": 200, "message": "Hello"}
    except Exception as e:
        return {"status": 500, "message": f"Internal Server Error: {e}"}
