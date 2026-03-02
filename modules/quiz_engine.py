from groq import Groq
import json
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_quiz(topic, level):

    prompt = f"""
You are an educational quiz generator.

Generate 5 multiple choice questions STRICTLY about the subject: {topic}.

Difficulty level: {level}.

Return ONLY valid JSON in this format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "answer": "Correct Option EXACT TEXT"
    }}
  ]
}}

Rules:
- Questions must be clearly related to {topic}.
- The answer must exactly match one of the options.
- Do NOT return A/B/C/D.
- No explanations.
- No text outside JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception as e:
        print("RAW AI OUTPUT:", content)
        print("ERROR:", e)
        return None