from groq import Groq
from together import Together
from agents.humanizer import humanize_sop
from agents.critic import critic_rewrite
from agents.cv_parser import parse_cv
import os

# Initialize AI clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def formal_prompt_template(student_name, course, university, cv_text):

    return f"""
Student {student_name} wants to pursue {course} at {university}.
I am providing his/her resume along with a required structure.
You must write a complete Letter of Motivation in paragraph form only.

Important Instructions:

1. Why This Course section must contain exactly 7 proper sentences (each sentence ending with "." counts as a line).
2. Why Germany section must contain exactly 6 proper sentences.
3. Why This Specific University section must contain exactly 6 proper sentences.
4. Write everything in first person.
5. Do not use headings in the final output.
6. Convert everything into paragraph form only.
7. Keep language natural and realistic.

Structure:

Introduction – include student name, course name and university.

Academic Background – bachelor, master if present, subjects, 10th and 12th.

Projects – explain important projects technically.

Professional Experience – internships and work experience.

Technical Certifications, Trainings, Workshops.

Extra Curricular Activities and Languages.

Why This Course - explain academic motivation clearly (7 sentences). 
Describe how the student's interest in this field developed and connect it with previous academic background, projects, or experiences. 
If the chosen course aligns with the bachelor's degree, explain deeper specialization. 
If it is different from the bachelor's degree, explain the transition logically. 
Also include 2–3 sentences describing the learning outcomes or knowledge the student expects to gain from this program.

Why Germany - explain why the student prefers Germany for higher education (6 sentences). 
Focus only on academic quality, research-oriented universities, interdisciplinary learning, and the international academic environment. 
Do NOT mention jobs, internships, big companies, low tuition fees, or comparisons with other countries.

Why This University – justify this university specifically (6 sentences).

Future Career Perspectives.

Conclusion.

Resume:
{cv_text}

Generate the Letter of Motivation now.
"""


# ---------- Utility Functions ----------

def remove_banned_connectors(text):

    banned = [
        "Moreover",
        "Furthermore",
        "Additionally",
        "In addition",
        "On the other hand",
        "Therefore",
        "Thus"
    ]

    for word in banned:
        text = text.replace(word, "")

    return text


def ensure_learning_outcomes(sop_text):

    keywords = [
        "learn",
        "knowledge",
        "skills",
        "develop",
        "understanding",
        "expertise"
    ]

    for word in keywords:
        if word.lower() in sop_text.lower():
            return sop_text

    extra = (
        " Through this program, I expect to deepen my theoretical understanding "
        "and develop practical skills relevant to the field. The curriculum will "
        "help me strengthen my analytical thinking and build expertise required "
        "for advanced academic and professional work."
    )

    return sop_text + extra


# ---------- AI Generation ----------

def generate_with_groq(prompt):

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200
    )

    return response.choices[0].message.content


def generate_with_together(prompt):

    response = together_client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200
    )

    return response.choices[0].message.content


# ---------- Main SOP Generator ----------

def generate_sop(student_name, course, university, cv_text, mode):

    structured_cv = parse_cv(cv_text)

    prompt = formal_prompt_template(student_name, course, university, structured_cv)

    try:
        # Try Groq first
        sop = generate_with_groq(prompt)

    except Exception as e:

        print("Groq failed. Switching to Together AI.")

        # Backup AI
        sop = generate_with_together(prompt)

    # Post processing pipeline
    sop = remove_banned_connectors(sop)

    sop = ensure_learning_outcomes(sop)

    sop = humanize_sop(sop)

    sop = critic_rewrite(sop)

    return sop
