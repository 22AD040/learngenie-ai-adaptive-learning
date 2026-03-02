import streamlit as st
import json
import os
from modules.content_engine import generate_content
from modules.quiz_engine import generate_quiz
from modules.adaptive_engine import update_level

st.set_page_config(page_title="LearnGenie AI", layout="wide")

# ================= DATABASE =================

DB_PATH = "database/users.json"

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

with open(DB_PATH, "r") as f:
    users = json.load(f)

# ================= SESSION STATES =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

# ================= LOGIN / REGISTER =================

if not st.session_state.logged_in:

    st.title("Login / Register")

    option = st.radio("Choose Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Register":
        if st.button("Register"):
            if username in users:
                st.error("User already exists")
            else:
                users[username] = {
                    "password": password,
                    "level": "Beginner"
                }
                with open(DB_PATH, "w") as f:
                    json.dump(users, f)
                st.success("Registered successfully")

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ================= MAIN APP =================

else:

    st.title("🧠 LearnGenie AI")
    st.subheader("Adaptive Personalized Learning Platform")

    st.write(f"Welcome, {st.session_state.username}")

    phase = st.selectbox("Select Phase", ["School", "College"])

    topic = st.text_input("Enter Topic")
    level = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

    # ================= CONTENT =================

    if st.button("Generate Study Material"):
        if topic:
            content = generate_content(topic, level, phase)
            st.markdown(content)
        else:
            st.warning("Please enter topic")

    # ================= QUIZ =================

    if st.button("Generate Quiz"):
        if topic:
            quiz = generate_quiz(topic, level)
            if quiz:
                st.session_state.quiz_data = quiz
                for key in list(st.session_state.keys()):
                    if key.startswith("q_"):
                        del st.session_state[key]
            else:
                st.error("Quiz generation failed")
        else:
            st.warning("Please enter topic")

    # ================= DISPLAY QUIZ =================

    if st.session_state.quiz_data:

        st.subheader("Answer the Quiz")

        user_answers = {}

        for i, q in enumerate(st.session_state.quiz_data["questions"]):
            st.write(f"**Q{i+1}: {q['question']}**")

            user_choice = st.radio(
                "Select your answer:",
                q["options"],
                index=None,
                key=f"q_{i}"
            )

            user_answers[i] = user_choice

        if st.button("Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.quiz_data["questions"]):

                user_ans = user_answers[i]
                correct_ans = q["answer"]

                if (
                    user_ans
                    and user_ans.strip().lower()
                    == correct_ans.strip().lower()
                ):
                    score += 1

            total_questions = len(st.session_state.quiz_data["questions"])
            percentage = (score / total_questions) * 100

            st.success(f"Your Score: {score}/{total_questions}")
            st.info(f"Percentage: {percentage}%")

            new_level = update_level(percentage)
            st.warning(f"Recommended Level: {new_level}")

            # Save recommended level
            users[st.session_state.username]["level"] = new_level
            with open(DB_PATH, "w") as f:
                json.dump(users, f)

    # ================= LOGOUT =================

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()