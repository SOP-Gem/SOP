from groq import Groq
from together import Together
import os

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def humanize_sop(sop_text):

    prompt = f"""
Rewrite the following SOP in a more natural, human, emotional tone.

Rules:
- Keep it professional.
- Keep first person.
- Maintain same facts and meaning.
- Reduce AI-like patterns.
- Vary sentence length naturally.
- Avoid robotic connectors like Moreover, Furthermore, Additionally.

SOP:
{sop_text}
"""

    # Try GROQ first
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=2000
        )

        return response.choices[0].message.content

    # If GROQ fails → use Together
    except Exception:

        response = together_client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=2000
        )

        return response.choices[0].message.content
