from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_content(topic, level, mode):

    prompt = f"""
You are an AI teacher.

Create structured study material for the following:

Topic: {topic}
Level: {level}
Education Mode: {mode}

Include the following sections clearly:

1. Explanation
2. Examples
3. Key Points
4. Summary

Make the explanation easy to understand for the selected level.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content