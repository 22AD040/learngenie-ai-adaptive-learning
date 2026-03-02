# 🧠 LearnGenie AI

Adaptive AI-Powered Personalized Learning Platform

---

## 🚀 Features

- 🔐 Login / Register System
- 🎓 School & College Mode
- 📚 AI Study Material Generation
- 📝 AI Quiz Generation
- 📊 Automatic Evaluation
- 🎯 Adaptive Difficulty Recommendation
- 💾 User Progress Saved (JSON Database)

---

## 🛠 Tech Stack

- Python 3.12
- Streamlit
- Groq API (LLaMA 3.1 Model)
- JSON Database
- dotenv

---

## 📂 Project Structure

```
learngenie-ai/
│
├── app.py
├── .env.example
├── requirements.txt
│
├── modules/
│   ├── content_engine.py
│   ├── quiz_engine.py
│   ├── adaptive_engine.py
│
├── database/
│   └── users.json
│
├── styles/
│   └── theme.css
│
└── assets/
    └── background.jpg
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/learn-genie-ai.git
cd learn-genie-ai
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add environment variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🌍 Deployment (Streamlit Cloud)

1. Push project to GitHub
2. Deploy on Streamlit Cloud
3. Add GROQ_API_KEY inside Secrets

---

## 📈 Future Improvements

- Leaderboard
- Mind Map Generation
- Audio Learning Mode
- Progress Analytics Dashboard
- PDF Export

---

## 📜 License

MIT License