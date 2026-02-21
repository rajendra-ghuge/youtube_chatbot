 YouTube Chatbot

An AI-powered YouTube assistant that extracts transcripts from YouTube videos, generates summaries, answers questions, and compares two videos intelligently using LLMs.

 Features

✅ Extract YouTube video transcripts

✅ Generate AI-powered summaries

✅ Ask questions about video content

✅ Compare two YouTube videos

✅ Clean React frontend

✅ FastAPI backend

✅ Persistent transcript storage

✅ Markdown formatted responses

Tech Stack
🔹 Frontend

React.js

Axios

React Router

React Markdown

🔹 Backend

FastAPI

Python

YouTube Transcript API

OpenAI / LLM integration

🔹 Database (Optional / Extendable)

Vector Database (for storing transcripts)

SQLite / PostgreSQL (for metadata storage)

Project Structure

youtube_chatbot/
│
├── backend/
│   ├── main.py
│   ├── transcript.py
│   ├── compare.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── Pages/
│   │   ├── Components/
│   │   └── App.jsx
│   └── package.json
│
└── README.md

⚙️ Installation & Setup
🔹 1️⃣ Clone the Repository
git clone https://github.com/your-username/youtube_chatbot.git
cd youtube_chatbot
🔹 2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Run backend:

uvicorn main:app --reload
🔹 3️⃣ Frontend Setup
cd frontend
npm install
npm run dev
