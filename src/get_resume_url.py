from supabase import create_client, Client

def get_resume_url(resume_path: str, url: str ,key: str) -> str | None:
    supabase: Client = create_client(url, key)
    try:
        response = supabase.storage.from_("resumes").create_signed_url(resume_path, 3600)
        if response.get("signedURL"):
            return response["signedURL"]
        else:
            print("Failed to get signed URL:", response)
            return None
    except Exception as e:
        print("Error getting signed URL:", e)
        return None