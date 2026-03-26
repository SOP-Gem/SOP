def build_sop_prompt(student_name, course, university, cv_analysis):
    return f"""
Write a Letter of Motivation for {student_name} applying for {course} at {university}.

Structure:

1. Introduction
2. Academic Background
3. Professional Experience
4. Why This Course (7 proper lines ending with ".")
5. Why Germany (6 proper lines ending with ".")
6. Why This University (6 proper lines ending with ".")
7. Future Career Goals
8. Conclusion

Write in FIRST PERSON only.

Use the following CV details:

{cv_analysis}
"""
