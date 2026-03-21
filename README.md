Prompt-Driven Email Productivity Agent
1. Problem

Managing emails is time-consuming and repetitive. People spend a lot of time categorizing emails, identifying action items, and drafting replies. Most email tools are static and cannot adapt to a user’s workflow or communication style.

The problem this project solves is:

Automatically categorize emails
Extract action items and deadlines
Draft email replies
Allow users to interact with emails using chat
Make the system customizable without changing code

This project explores how LLMs + prompts can be used to build a flexible email productivity assistant.

2. Approach

I built a prompt-driven AI email agent where all AI behavior is controlled by prompts stored in JSON instead of hardcoded logic.

System workflow:

Emails are loaded (mock inbox or Gmail API).
Emails are sent to Gemini API with categorization prompt.
Action items and deadlines are extracted using another prompt.
Draft replies are generated using auto-reply prompt.
A chat agent allows users to interact with emails (summarize, list tasks, draft replies).
All prompts can be edited in the UI (“Prompt Brain”), which changes AI behavior without changing code.

Tech architecture:

Frontend: React + Tailwind (UI with Inbox, Chat, Drafts, Prompts tabs)
Backend: Flask (REST APIs)
LLM: Google Gemini API
Storage: JSON database (emails, prompts, drafts, actions)
3. Iterations

This project was built in multiple iterations:

Iteration 1: Basic Email Categorization

Load mock emails
Categorize emails using LLM

Iteration 2: Action Item Extraction

Extract tasks and deadlines from emails
Store structured output in JSON

Iteration 3: Auto-Reply Draft Generator

Generate reply drafts for emails
Store drafts for review (never auto-send)

Iteration 4: Chat-Based Email Agent

Chat interface to summarize emails and list tasks
Ask questions like “What are my urgent emails?”

Iteration 5: Prompt Brain

UI where users can edit prompts
Changing prompts changes AI behavior dynamically
4. Key Design Choices

Some important design decisions:

Prompt-Driven Architecture: All AI behavior controlled via prompts in JSON instead of hardcoding logic.
JSON Database Instead of SQL: Chosen for simplicity and fast prototyping.
Drafts Not Auto-Sent: For safety and human review.
Mock Inbox First: System works without Gmail API to make testing easy.
Modular Backend: Separate files for database, LLM service, Gmail service.
Editable Prompt UI: Makes system flexible and user-controlled.

These decisions made the system flexible, safe, and easy to extend.

5. Daily Time Commitment

I spent approximately 2–3 hours per day working on this project, including:

Designing prompts
Building backend APIs
Developing React UI
Testing LLM outputs
Improving prompt accuracy and UX

Total development time: ~3–4 weeks.

6. Impact

This project demonstrates:

Real-world use of LLMs in productivity tools
Prompt engineering and AI workflow design
Full-stack AI application development
Building a customizable AI agent system

The system can be extended into a real AI email assistant SaaS product.

If you want, next I can help you write the GitHub README intro + screenshots section (that increases selection chances a lot).

make it look like readme file for github

Here is your GitHub README.md properly formatted. You can paste this directly into your repository.

📧 Prompt-Driven Email Productivity Agent

An intelligent, prompt-driven Email Productivity Agent that automates email management using AI. The system processes a real or mock inbox and performs:

Email categorization
Action-item extraction
Auto-drafting replies
Chat-based inbox interaction

All LLM-powered operations are controlled by user-defined prompts (“the agent brain”), which are stored and editable in the UI.

🔗 Live Demo: https://email-productivity-frontend.onrender.com/

🧠 Problem

Managing emails is time-consuming and repetitive. Users spend a lot of time categorizing emails, identifying action items, and drafting replies. Most email tools are static and cannot adapt to a user’s workflow or communication style.

This project solves:

Automatically categorize emails
Extract action items and deadlines
Draft email replies
Allow users to interact with emails using chat
Make the system customizable without changing code

This project explores how LLMs + Prompt Engineering can be used to build a flexible email productivity assistant.

🛠️ Approach

I built a prompt-driven AI email agent where all AI behavior is controlled by prompts stored in JSON instead of hardcoded logic.

System Workflow
Emails are loaded (mock inbox or Gmail API).
Emails are categorized using Gemini API.
Action items and deadlines are extracted.
Draft replies are generated.
A chat agent allows users to interact with emails.
Prompts can be edited in the UI (“Prompt Brain”), which changes AI behavior without changing code.
Tech Architecture

Frontend

React
TailwindCSS
Vite

Backend

Python
Flask

LLM

Google Gemini API

Storage

JSON (emails, prompts, drafts, actions)
🔄 Iterations

This project was built in multiple iterations:

Iteration 1 – Email Categorization

Load mock emails
Categorize emails using LLM

Iteration 2 – Action Item Extraction

Extract tasks and deadlines
Store structured output

Iteration 3 – Auto-Reply Draft Generator

Generate reply drafts
Store drafts for review

Iteration 4 – Chat-Based Email Agent

Chat interface to summarize emails and list tasks

Iteration 5 – Prompt Brain

UI where users can edit prompts
Changing prompts changes AI behavior dynamically
🧱 Key Design Choices
Prompt-Driven Architecture – AI behavior controlled via prompts instead of hardcoded logic.
JSON Database – Used for fast prototyping and simplicity.
Drafts Not Auto-Sent – For safety and human review.
Mock Inbox First – System works without Gmail API for easy testing.
Modular Backend – Separate modules for database, LLM, and Gmail service.
Editable Prompt UI – Makes system flexible and customizable.
⏱️ Daily Time Commitment

I spent approximately 2–3 hours per day working on this project, including:

Prompt design
Backend API development
React UI development
Testing LLM outputs
Improving prompt accuracy and UX

Total development time: ~3–4 weeks

📊 Impact

This project demonstrates:

Real-world use of LLMs in productivity tools
Prompt engineering and AI workflow design
Full-stack AI application development
Building a customizable AI agent system

The system can be extended into a real AI email assistant SaaS product.

🚀 Tech Stack
Backend
Python
Flask
Google Generative AI (Gemini)
Gmail API (optional)
JSON storage
Frontend
React
TailwindCSS
Vite
Node.js
▶️ Running the Project
Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app.py

Backend runs on: http://localhost:5001

Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs on: http://localhost:5173

📌 Features
Load Mock Inbox
Gmail Integration (Optional)
Email Categorization (AI)
Action Item Extraction
AI Reply Draft Generator
Chat with Email Agent
Prompt Editing (“Prompt Brain”)
Draft Management System


❤️ Built By
Shristi Shrivastava
GitHub: https://github.com/shri2310sti
LinkedIn: https://www.linkedin.com/in/shristishrivastava1
