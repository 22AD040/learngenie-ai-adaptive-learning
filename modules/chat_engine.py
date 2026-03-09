from modules.config import client


def ask_ai(topic, question):

    prompt = f"""
You are an AI tutor helping students understand concepts.

Topic: {topic}

Student Question:
{question}

Explain clearly with simple examples.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful tutor."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content