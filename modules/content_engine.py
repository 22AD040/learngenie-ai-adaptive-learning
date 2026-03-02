from groq import Groq
import streamlit as st

# Use Streamlit secrets (works in deployment)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_content(topic, level, mode):

    prompt = f"""
    You are an AI teacher.

    Create structured study material for:

    Topic: {topic}
    Level: {level}
    Mode: {mode} (School or College)

    Include:
    - Explanation
    - Examples
    - Key Points
    - Summary
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content