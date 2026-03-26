from groq import Groq
from together import Together
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
together_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def critic_rewrite(sop_text):

    prompt = f"""
You are an expert academic editor.

Your task is to rewrite the SOP so it sounds more like a real student wrote it.

Guidelines:
- Keep first person.
- Maintain all facts.
- Slightly vary sentence lengths.
- Avoid repetitive academic AI patterns.
- Make the tone natural but still professional.
- Do not shorten the SOP.
- Do not remove important information.

SOP:
{sop_text}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception:

        response = together_client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=2000
        )

        return response.choices[0].message.content
