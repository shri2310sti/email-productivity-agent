# 📧 Prompt-Driven Email Productivity Agent

An intelligent, prompt-driven Email Productivity Agent that automates email management using AI. The system processes a real or mock inbox and performs:

- Email categorization  
- Action-item extraction  
- Auto-drafting replies  
- Chat-based inbox interaction  

All LLM-powered operations are controlled by user-defined prompts (“the agent brain”), which are stored and editable in the UI.

Link :- https://email-productivity-frontend.onrender.com/

***

## 🧱 Tech Stack

### Backend

- Python 3.8+  
- Flask  
- Google Generative AI (Gemini)  
- Gmail API (optional for real inbox ingestion)  
- JSON-based storage for:
  - Emails  
  - Extracted action items  
  - Drafts  
  - Prompt templates  

### Frontend

- Node.js 16+  
- React 18  
- Vite  
- TailwindCSS  

***

## 📁 Project Structure

```text
email-productivity-agent/
├── backend/
│   ├── app.py                  # Flask API server (all endpoints)
│   ├── database.py             # JSON database management (emails, drafts, prompts)
│   ├── llm_service.py          # Gemini LLM integration using stored prompts
│   ├── gmail_service.py        # Gmail API integration (optional, real inbox)
│   ├── mock_inbox.json         # Mock Inbox with 20 sample emails (assignment: 10–20)
│   ├── default_prompts.json    # Default prompt templates (categorization, action-item, auto-reply, chat)
│   ├── data.json               # Runtime data storage (processed categories, actions, drafts)
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component, 4-tab UI
│   │   ├── services/
│   │   │   └── api.js          # API client for backend endpoints
│   │   └── main.jsx            # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

***

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd email-productivity-agent
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a **`.env`** file in `backend`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
PORT=5001
```

**Gemini API key:**

1. Visit https://makersuite.google.com/app/apikey  
2. Create an API key  
3. Paste it into `.env` as `GEMINI_API_KEY`  

#### Optional: Gmail Integration

To use real Gmail instead of only mock data:

1. Go to Google Cloud Console and create a project.  
2. Enable **Gmail API**.  
3. Create OAuth 2.0 credentials.  
4. Download `credentials.json` and place it in `backend/`.  
5. On first run, the app will prompt you to authenticate and create a token file.

### 3. Frontend Setup

```bash
cd frontend
npm install
```

***

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
python app.py
```

Backend runs on: `http://localhost:5001`

### Start Frontend (UI)

In another terminal:

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:5173`

***

## 📚 Assignment Output & Assets

### 1. Source Code Repository

- Full application code (backend + frontend) in this repository with clear separation of:
  - UI  
  - Backend services  
  - State management (JSON)  
  - LLM integration (Gemini)  

### 2. README.md Includes

- Full **setup instructions** (backend & frontend).  
- How to **run the UI and backend**.  
- How to **load the Mock Inbox**.  
- How to **configure prompts**.  
- **Usage examples** and test cases.

### 3. Project Assets

- **Mock Inbox**:  
  - `backend/mock_inbox.json` with **20 sample emails** (assignment requirement: 10–20).  
  - Includes:
    - Meeting requests  
    - Newsletters  
    - Spam-like messages  
    - Task requests  
    - Project updates  

- **Default Prompt Templates**:  
  - `backend/default_prompts.json` includes prompts for:
    - Categorization  
    - Action-item extraction  
    - Auto-reply draft generation  
    - Chat / Email Agent behavior  

Example prompt semantics implemented:

- **Categorization Prompt**  
  - Categorizes emails into: `Important`, `Newsletter`, `Spam`, `To-Do`.  
  - To-Do emails contain direct user action.  

- **Action Item Extraction Prompt**  
  - Extracts tasks and deadlines, returning structured JSON, e.g.:  
    - `{ "task": "...", "deadline": "..." }`  

- **Auto-Reply Draft Prompt**  
  - For meeting requests, drafts a polite reply asking for agenda and availability details.  

- **Chat Prompt**  
  - Guides how the Email Agent summarizes, lists tasks, drafts replies, and answers questions about the inbox.

***

## 🧠 Prompt-Driven Architecture

The system is explicitly **prompt-driven**:

- All prompts are **stored** in JSON (`default_prompts.json` + `data.json`).  
- The **Prompts** tab in the UI exposes a **“Prompt Brain” panel** where users can:
  - View current prompts.  
  - Edit categorization, action-item, auto-reply, and chat prompts.  
  - Save changes.  

All LLM operations use these stored prompts:

- Email categorization  
- Action-item extraction  
- Auto-drafting replies  
- Chat-based responses  

Changing the prompts directly changes the behavior of the agent without code changes.

***

## 🧪 Functional Requirements & Phases

### Phase 1: Email Ingestion & Knowledge Base

**UI Features**

- **Load Emails**:
  - Load **Mock Inbox** (default, no Gmail required).  
  - Optionally fetch real Gmail emails via Gmail API.  
- **Inbox View**:
  - Display **sender**, **subject**, **timestamp**, and **category tags** after processing.  
- **Prompt Configurations**:
  - “Prompt Brain” panel (Prompts tab) with:
    - Categorization Prompt  
    - Action Item Prompt  
    - Auto-Reply Draft Prompt  
    - Chat Prompt  

**Backend Logic**

- Stores prompts and processed outputs in JSON (`data.json`):  
  - Categories  
  - Extracted action items  
  - Drafts  
- Ingestion Pipeline:
  1. Load emails (mock or Gmail).  
  2. Run categorization prompt via Gemini.  
  3. Run action-item prompt via Gemini.  
  4. Save results in JSON.  
  5. Update UI via API.

### Phase 2: Email Processing Agent (Email Agent / Chat)

**UI Features**

- **Chat Tab (Email Agent)**:
  - Select an email from Inbox.  
  - Ask:
    - “Summarize this email.”  
    - “What tasks do I need to do?”  
    - “Draft a reply based on my tone.”  
    - “Show me all urgent emails.”  

**Agent Logic**

1. Agent receives:
   - User query  
   - Selected email content  
   - Relevant stored prompts  
2. Constructs LLM request combining:
   - Email text  
   - Prompt (categorization, action, reply, or chat)  
   - User instruction  
3. LLM returns structured or natural-language output.  
4. Response shown in Chat tab.

### Phase 3: Draft Generation Agent

**UI Features**

- **Drafts Tab**:
  - Generate new email drafts from Inbox or Chat.  
  - View, edit, and save drafts.  
  - Delete drafts if not needed.  

**Agent Logic**

- For drafting replies:
  - Uses **user’s auto-reply prompt**.  
  - Uses **email thread context** when replying.  
  - **Never sends emails automatically**.  
  - Stores draft subject, body, and metadata for review.

**Draft Output**

Each draft includes:

- Subject  
- Body  
- Optional suggested follow-ups  
- JSON metadata (e.g., linked category/action info)

***

## 🔌 API Endpoints

### Email Management

- `POST /api/emails/load-mock` – Load mock inbox from `mock_inbox.json`  
- `GET /api/emails/fetch` – Fetch from Gmail (optional)  
- `POST /api/emails/process` – Process all emails with AI (categorization + actions)  
- `GET /api/emails` – Get all emails and their metadata  

### Chat & Drafts

- `POST /api/chat` – Chat with the Email Agent about a selected email or inbox  
- `POST /api/draft/generate` – Generate auto-draft reply for an email  
- `GET /api/drafts` – List stored drafts  
- `DELETE /api/drafts/<id>` – Delete a draft  

### Prompt Configuration

- `GET /api/prompts` – Get all stored prompts  
- `PUT /api/prompts` – Update prompts (Prompt Brain)  
- `POST /api/prompts/reset` – Reset to default_prompts.json  

### System

- `GET /api/health` – Health check endpoint  

***

## 📊 Usage Workflow & Examples

### 1. Load Mock Inbox (Recommended First)

1. Open `http://localhost:5173`.  
2. Click **“Load Mock Inbox”**.  
3. 20 sample emails appear from `mock_inbox.json`.  
4. Click **“Process All”** to run categorization + action-item extraction.

### 2. Work with Inbox

- Browse emails in **Inbox** tab.  
- Check categories:
  - Example mappings:
    - “Q4 Project Deadline” → To-Do  
    - “Weekly Tech Digest” → Newsletter  
    - “YOU WON $1,000,000” → Spam  
    - “Urgent: Bug in Production” → Important  
- Select an email to view full details and action items.  
- Generate draft replies from Inbox.

### 3. Email Agent Chat

- Go to **Chat** tab.  
- Select an email and ask:
  - “Summarize this email in 2 sentences.”  
  - “What actions do I need to take?”  
  - “What’s the deadline?”  
  - “Draft a reply confirming the meeting.”  

### 4. Manage Drafts

- Go to **Drafts** tab.  
- Review all generated draft replies.  
- Edit content manually in your email client.  
- Delete drafts that are not needed.  
- Drafts are **never** auto-sent.

### 5. Configure Prompts (Prompt Brain)

- Go to **Prompts** tab.  
- Edit:
  - Categorization Prompt  
  - Action Item Extraction Prompt  
  - Auto-Reply Prompt  
  - Chat Prompt  
- Save changes.  
- Re-run **“Process All”** on inbox to see new behavior (e.g., stricter spam rules, different tone in replies).

***

## 🛡️ Safety, Robustness & Evaluation Criteria

- **Functionality**:
  - Inbox ingestion from mock or Gmail.  
  - Prompt-based email categorization and parsing.  
  - LLM generates summaries, replies, and suggestions.  
  - Drafts safely stored as drafts (JSON), not sent.  

- **Prompt-Driven Architecture**:
  - Users can create, edit, and save prompts via the Prompts tab.  
  - All LLM behavior depends on stored prompts (no hard-coded system behavior).  

- **Code Quality**:
  - Clear separation of UI (React), backend (Flask), LLM integration (llm_service.py), and storage (database.py).  
  - Modular and readable code designed for extension.  

- **User Experience**:
  - Clean prompt configuration panel.  
  - Intuitive inbox viewer with categories and action items.  
  - Smooth Email Agent chat experience.  

- **Safety & Robustness**:
  - LLM/API errors handled gracefully with appropriate UI feedback.  
  - Application always defaults to **drafting**, never sending.  
  - Optional Gmail integration; mock inbox is always available.

***

Made with ❤️ for AI-powered, **prompt-driven** email productivity.
