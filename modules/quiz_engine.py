from groq import Groq
import os
import json
import re
import random
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):

    match = re.search(r'\{.*\}', text, re.DOTALL)

    if match:
        return match.group(0)

    return None


def fix_options(options, answer):

    options = [str(o).strip() for o in options]
    answer = str(answer).strip()

    options = list(dict.fromkeys(options))

    if answer not in options:
        options.append(answer)

    while len(options) < 4:
        options.append("None of the above")

    options = options[:4]

    random.shuffle(options)

    return options, answer


def generate_quiz(topic, level, education, std=None):

    if education == "School":
        difficulty_context = f"For a Class {std} student."
    else:
        difficulty_context = "For a college student."

    prompt = f"""
You are an expert teacher.

Generate EXACTLY 5 multiple choice questions.

Topic: {topic}
Difficulty Level: {level}
Student Level: {difficulty_context}

Rules:

1. Questions must be factually correct.
2. Each question must have exactly 4 options.
3. Only ONE option must be correct.
4. The correct answer MUST appear in the options.
5. All options must be different.
6. Include a SHORT explanation for the correct answer.

Return ONLY JSON in this format:

{{
 "questions":[
  {{
   "question":"Question text",
   "options":["option1","option2","option3","option4"],
   "answer":"correct option text",
   "explanation":"simple explanation of why the answer is correct"
  }}
 ]
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()

        json_text = extract_json(content)

        if json_text is None:
            return None

        quiz = json.loads(json_text)

        validated_questions = []

        for q in quiz.get("questions", []):

            question = str(q.get("question", "")).strip()
            options = q.get("options", [])
            answer = str(q.get("answer", "")).strip()
            explanation = str(q.get("explanation", "")).strip()

            options, answer = fix_options(options, answer)

            validated_questions.append({
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation
            })

        if len(validated_questions) >= 5:
            return {"questions": validated_questions[:5]}

        return None

    except Exception as e:
        print("Quiz generation error:", e)
        return None