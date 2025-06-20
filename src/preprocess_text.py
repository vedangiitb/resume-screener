import re

def clean_resume_point(text: str) -> str:
    # 1. Remove common bullet symbols
    text = re.sub(r"[•▪●–—]", "", text)

    # 2. Replace pipe-like separators with commas
    text = text.replace("|", ",").replace("¦", ",")

    # 3. Remove multiple consecutive spaces/tabs
    text = re.sub(r"\s+", " ", text)

    # 4. Remove unwanted punctuation at start/end
    text = text.strip(" ,.-")

    return text.strip()


def preprocess_text(points):
    if not points:
        return []
    non_empty_points = filter(lambda s: s != "", points)
    filtered_points = list(non_empty_points)
    filtered_points = [clean_resume_point(point) for point in filtered_points]
    return filtered_points