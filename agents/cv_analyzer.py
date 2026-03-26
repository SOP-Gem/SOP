def analyze_cv(cv_text):
    prompt = f"""
    Analyze the following CV and extract:
    - Academic Background
    - Work Experience
    - Projects
    - Certifications
    - Skills
    - Languages

    CV:
    {cv_text}
    """
    return prompt
