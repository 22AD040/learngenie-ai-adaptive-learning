import streamlit as st
import json
import os
import altair as alt
import pandas as pd
from streamlit_tags import st_tags
from streamlit_agraph import agraph, Node, Edge, Config

from modules.content_engine import generate_content
from modules.quiz_engine import generate_quiz
from modules.mindmap_engine import generate_mindmap_explanation, extract_sections, extract_points
from modules.pdf_engine import create_pdf
from modules.adaptive_engine import update_level
from modules.recommendation_engine import recommend_study_materials
from modules.chat_engine import ask_ai

st.set_page_config(page_title="LearnGenie AI", layout="wide")

DATABASE_FILE="database/users.json"

st.markdown("""
<style>

.stApp{
background:#f4f6fb;
font-family:'Segoe UI';
}

.main-header{
text-align:center;
font-size:40px;
font-weight:700;
margin-top:10px;
color:#111827;
}

.sub-header{
text-align:center;
color:#6b7280;
margin-bottom:30px;
font-size:16px;
}

[data-testid="stSidebar"]{
background:#1f3aed;
}

.resource-card{
background:white;
padding:20px;
border-radius:12px;
margin-bottom:18px;
box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

.profile-box{
background:white;
padding:25px;
border-radius:12px;
margin-bottom:20px;
box-shadow:0px 4px 12px rgba(0,0,0,0.08);
font-size:16px;
}

.stButton>button{
background:#2563eb;
color:white;
border-radius:8px;
border:none;
padding:8px 18px;
font-weight:500;
}

.stButton>button:hover{
background:#1e40af;
}

</style>
""", unsafe_allow_html=True)


if "quiz_data" not in st.session_state:
    st.session_state.quiz_data=None

if "content" not in st.session_state:
    st.session_state.content=None

if "topic" not in st.session_state:
    st.session_state.topic=""


def load_users():

    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE,"r") as f:
            users=json.load(f)
    else:
        users={}

    for u in users:

        if "history" not in users[u]:
            users[u]["history"]=[]

        if "scores" not in users[u]:
            users[u]["scores"]=[]

        if "streak" not in users[u]:
            users[u]["streak"]=1

    return users


def save_users(users):

    with open(DATABASE_FILE,"w") as f:
        json.dump(users,f,indent=4)


users=load_users()


if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "username" not in st.session_state:
    st.session_state.username=None


if not st.session_state.logged_in:

    col1,col2,col3=st.columns([2,3,2])

    with col2:

        st.markdown("<h1 class='main-header'>LearnGenie AI</h1>",unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>AI Powered Personalized Learning</p>",unsafe_allow_html=True)

        option=st.radio("Select Option",["Login","Register"],horizontal=True)

        username=st.text_input("Username")
        password=st.text_input("Password",type="password")

        if option=="Register":

            name=st.text_input("Full Name")
            edu_type=st.selectbox("Education Type",["School","College"])

            if edu_type=="School":
                std=st.selectbox("Class",["6","7","8","9","10","11","12"])
                stream=None
                dept=None
            else:
                std=None
                stream=st.selectbox("Stream",["Engineering","Arts","Science","Commerce"])
                dept=st.text_input("Department")

            if st.button("Register"):

                if username in users:
                    st.error("User already exists")

                else:

                    users[username]={
                        "password":password,
                        "name":name,
                        "education":edu_type,
                        "std":std,
                        "stream":stream,
                        "dept":dept,
                        "level":"Beginner",
                        "history":[],
                        "scores":[],
                        "streak":1
                    }

                    save_users(users)
                    st.success("Registration Successful")

        if option=="Login":

            if st.button("Login"):

                if username in users and users[username]["password"]==password:

                    st.session_state.logged_in=True
                    st.session_state.username=username
                    st.rerun()

                else:
                    st.error("Invalid Login")


else:

    user=users[st.session_state.username]

    name=user.get("name","Student")
    education=user.get("education")
    std=user.get("std")
    stream=user.get("stream")
    dept=user.get("dept")
    history=user.get("history",[])
    scores=user.get("scores",[])
    streak=user.get("streak",1)

    st.sidebar.markdown("## LearnGenie AI")

    menu=st.sidebar.radio(
        "Navigation",
        [
            "User Profile",
            "Progress Dashboard",
            "Generate Study Material",
            "Mind Map",
            "Recommended Materials",
            "Generate Quiz",
            "AI Study Assistant",
            "Leaderboard"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.markdown('<div class="main-header">LearnGenie AI</div>',unsafe_allow_html=True)


    if menu=="User Profile":

        st.subheader("User Profile")

        if education=="School":

            st.markdown(f"""
            <div class="profile-box">
            <b>Name:</b> {name}<br>
            <b>Education:</b> School<br>
            <b>Class:</b> {std}<br>
            <b>Level:</b> {user.get("level")}
            </div>
            """,unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="profile-box">
            <b>Name:</b> {name}<br>
            <b>Education:</b> College<br>
            <b>Stream:</b> {stream}<br>
            <b>Department:</b> {dept}<br>
            <b>Level:</b> {user.get("level")}
            </div>
            """,unsafe_allow_html=True)

        st.success(f"🔥 Learning Streak: {streak} days")

        col1,col2,col3,col4=st.columns(4)

        col1.metric("Quizzes Taken",len(scores))

        avg_score=round(sum(scores)/len(scores),2) if scores else 0

        col2.metric("Average Score",avg_score)

        col3.metric("Learning Level",user.get("level"))

        col4.metric("Topics Learned",len(history))

        st.subheader("Previous Topics")

        if history:

            cols=st.columns(4)

            for i,topic_item in enumerate(history):

                with cols[i%4]:

                    if st.button(str(topic_item),key=str(topic_item)):
                        st.session_state.topic=topic_item
                        st.rerun()

        else:
            st.info("No previous topics yet.")


    elif menu=="Progress Dashboard":

        st.subheader("Learning Progress")

        if scores:

            df=pd.DataFrame({
                "Attempt":list(range(1,len(scores)+1)),
                "Score":scores
            })

            chart=alt.Chart(df).mark_line(point=True).encode(
                x="Attempt",
                y="Score"
            ).properties(width=700,height=400)

            st.altair_chart(chart)

        else:
            st.info("No quiz attempts yet.")

        st.success(f"Current Level: {user.get('level')}")


    elif menu=="Generate Study Material":

        suggested_topics=[
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Python Programming",
        "Neural Networks",
        "Data Science",
        "Natural Language Processing",
        "Computer Vision"
        ]

        topic=st_tags(
        label="Enter Topic",
        text="Press enter to add more",
        value=[st.session_state.topic] if st.session_state.topic else [],
        suggestions=suggested_topics
        )

        if topic:
            topic=topic[0]
        else:
            topic=""

        level=st.selectbox("Difficulty Level",["Beginner","Intermediate","Advanced"])

        if st.button("Generate Study Material"):

            if topic=="":

                st.warning("Please enter a topic")

            else:

                content=generate_content(topic,level,education)

                st.session_state.content=content
                st.session_state.topic=topic

                if topic not in history:
                    history.append(topic)
                    users[st.session_state.username]["history"]=history
                    save_users(users)

        if st.session_state.content:

            st.markdown(st.session_state.content)

            pdf_file=create_pdf(st.session_state.content)

            with open(pdf_file,"rb") as f:

                st.download_button(
                    "Download PDF",
                    f,
                    "study_material.pdf",
                    "application/pdf"
                )


    elif menu=="Mind Map":

        if st.session_state.content:

            st.subheader("Interactive Mind Map")

            sections=extract_sections(st.session_state.content)
            points=extract_points(st.session_state.content)

            nodes=[]
            edges=[]

            nodes.append(Node(id="Topic",label=st.session_state.topic,size=30))

            p_index=0

            for i,sec in enumerate(sections):

                sid=f"s{i}"

                nodes.append(Node(id=sid,label=sec,size=20))
                edges.append(Edge(source="Topic",target=sid))

                for j in range(2):

                    if p_index>=len(points):
                        break

                    point=points[p_index]
                    p_index+=1

                    pid=f"{sid}_{j}"

                    nodes.append(Node(id=pid,label=point,size=15))
                    edges.append(Edge(source=sid,target=pid))

            config=Config(width=900,height=500,directed=True,physics=True)

            agraph(nodes=nodes,edges=edges,config=config)

            explanation=generate_mindmap_explanation(
                st.session_state.topic,
                st.session_state.content
            )

            st.info(explanation)

        else:
            st.warning("Generate study material first.")


    elif menu=="Recommended Materials":

        st.subheader("Recommended Study Materials")

        if st.session_state.topic=="":
            st.warning("Generate study material first.")

        else:

            recommendations=recommend_study_materials(
                st.session_state.topic,
                "Beginner"
            )

            for item in recommendations:

                st.markdown(f"""
                <div class="resource-card">
                <b>{item["title"]}</b><br>
                {item["description"]}<br><br>
                <a href="{item["url"]}" target="_blank">Open Resource</a>
                </div>
                """,unsafe_allow_html=True)


    elif menu=="Generate Quiz":

        topic=st.session_state.topic

        if st.button("Generate Quiz"):

            if topic=="":
                st.warning("Generate study material first.")

            else:

                quiz=generate_quiz(topic,"Beginner",education,std)

                if quiz:
                    st.session_state.quiz_data=quiz


        if st.session_state.quiz_data:

            st.subheader("Quiz")

            total=len(st.session_state.quiz_data["questions"])

            for i,q in enumerate(st.session_state.quiz_data["questions"]):

                st.write(f"Q{i+1}: {q['question']}")

                st.radio(
                    "Select Answer",
                    q["options"],
                    index=None,
                    key=f"q{i}"
                )

            if st.button("Submit Quiz"):

                score=0

                for i,q in enumerate(st.session_state.quiz_data["questions"]):

                    user_answer=st.session_state.get(f"q{i}")
                    correct=q["answer"]
                    explanation=q.get("explanation","")

                    if user_answer==correct:
                        score+=1
                        st.success(f"Q{i+1} Correct")
                        st.info(f"Explanation: {explanation}")
                    else:
                        st.error(f"Q{i+1} Wrong")
                        st.info(f"Correct Answer: {correct}")
                        st.info(f"Explanation: {explanation}")

                percentage=(score/total)*100

                users[st.session_state.username]["scores"].append(percentage)

                st.success(f"Score {score}/{total}")

                new_level=update_level(percentage)

                users[st.session_state.username]["level"]=new_level

                save_users(users)


    elif menu=="AI Study Assistant":

        st.subheader("AI Study Assistant")

        if st.session_state.topic=="":
            st.warning("Generate study material first.")
        else:

            st.write(f"Current Topic: {st.session_state.topic}")

            question=st.text_input("Ask a question about this topic")

            if st.button("Ask AI"):

                if question:

                    with st.spinner("AI is thinking..."):

                        answer=ask_ai(st.session_state.topic,question)

                        st.markdown(answer)


    elif menu=="Leaderboard":

        st.subheader("Top Learners")

        leaderboard=[]

        for u in users:

            sc=users[u].get("scores",[])

            if sc:
                avg=sum(sc)/len(sc)
            else:
                avg=0

            leaderboard.append((u,avg))

        leaderboard.sort(key=lambda x:x[1],reverse=True)

        df=pd.DataFrame(leaderboard,columns=["User","Average Score"])

        st.dataframe(df)