import streamlit as st
from modules.content_engine import generate_content
from modules.quiz_engine import generate_quiz
from modules.adaptive_engine import update_level

st.set_page_config(page_title="LearnGenie AI", layout="wide")

# ================= SIMPLE IN-MEMORY DATABASE =================

if "users" not in st.session_state:
    st.session_state.users = {}

users = st.session_state.users

# ================= SESSION STATES =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "username" not in st.session_state:
    st.session_state.username = None

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
                st.success("Registered successfully")

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
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

    # ========== GENERATE STUDY MATERIAL ==========
    if st.button("Generate Study Material"):
        if topic:
            content = generate_content(topic, level, phase)
            st.markdown(content)
        else:
            st.warning("Please enter topic")

    # ========== GENERATE QUIZ ==========
    if st.button("Generate Quiz"):
        if topic:
            quiz = generate_quiz(topic, level)
            if quiz:
                st.session_state.quiz_data = quiz
            else:
                st.error("Quiz generation failed")
        else:
            st.warning("Please enter topic")

    # ========== DISPLAY QUIZ ==========
    if st.session_state.quiz_data:

        st.subheader("Answer the Quiz")

        total_questions = len(st.session_state.quiz_data["questions"])

        for i, q in enumerate(st.session_state.quiz_data["questions"]):

            st.write(f"### Q{i+1}: {q['question']}")

            st.radio(
                "Select your answer:",
                q["options"],
                index=None,
                key=f"q_{i}"
            )

        if st.button("Submit Quiz"):

            score = 0
            st.markdown("---")

            for i, q in enumerate(st.session_state.quiz_data["questions"]):

                user_answer = st.session_state.get(f"q_{i}")
                correct_answer = q["answer"]

                if user_answer == correct_answer:
                    score += 1
                    st.success(f"Q{i+1} ✅ Correct")
                else:
                    st.error(f"Q{i+1} ❌ Wrong")
                    st.info(f"Correct Answer: {correct_answer}")

            percentage = (score / total_questions) * 100

            st.markdown("## 🎯 Final Result")
            st.success(f"Score: {score}/{total_questions}")
            st.info(f"Percentage: {percentage}%")

            new_level = update_level(percentage)
            st.warning(f"Recommended Level: {new_level}")

            users[st.session_state.username]["level"] = new_level

    # ========== LOGOUT ==========
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()