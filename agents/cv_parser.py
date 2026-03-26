from groq import Groq
from together import Together
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def parse_cv(cv_text):

    prompt = f"""
You are an AI that extracts structured information from a student's CV.

Extract the following information:

1. Education
2. Projects
3. Internships
4. Work Experience
5. Technical Skills
6. Certifications
7. Workshops / Trainings
8. Extra Curricular Activities
9. Languages

Return the information clearly organized under these headings.

CV:
{cv_text}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception:

        response = together_client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content
