# 🤖 AI Research Assistant

A full-stack web application that performs deep research on any topic. It decomposes complex questions, searches the web in parallel using Tavily, and synthesizes a comprehensive answer using Grok (x-ai/grok-4.1-fast:free) via OpenRouter.

## ✨ Features

✅ **Query Decomposition**: Breaks down complex user questions into targeted sub-questions.  
✅ **Parallel Web Search**: Uses Tavily API to perform concurrent searches for speed.  
✅ **Smart Extraction**: Automatically extracts relevant content from URLs (no scraping code needed).  
✅ **LLM Synthesis**: Uses Grok (x-ai/grok-4.1-fast:free) to generate natural language answers.  
✅ **Citations**: Every claim is backed by a source URL.  
✅ **Rate Limit Handling**: Intelligent delays to respect free tier API limits.  
✅ **Modern UI**: Clean React interface styled with Tailwind CSS.

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI (Async/Await)
- **AI Model**: Grok (x-ai/grok-4.1-fast:free) via OpenRouter
- **Search Engine**: Tavily AI Search

### Frontend
- **Framework**: React (Vite)
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Node.js & npm

### 1. Backend Setup

Navigate to the backend folder:
```bash
cd backend
```

Create a virtual environment (recommended) and install dependencies:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Install libraries
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
TAVILY_API_KEY=tvly-your_tavily_key_here
```
*Get keys here: [OpenRouter](https://openrouter.ai/) | [Tavily](https://tavily.com/)*

Start the Python Server:
```bash
python main.py
```
*Server runs at: `http://localhost:8000`*

### 2. Frontend Setup

Open a new terminal and navigate to the frontend folder:
```bash
cd frontend
```

Install dependencies and start the UI:
```bash
npm install
npm run dev
```
*UI runs at: `http://localhost:5173`*

---

## 📖 Usage

1. Ensure both Backend and Frontend terminals are running.
2. Open `http://localhost:5173` in your browser.
3. Type a question (e.g., *"What are the latest breakthroughs in Solid State Batteries?"*).
4. Click **Search**.
5. The agent will:
   - Plan the research steps.
   - Search the web for multiple sub-topics.
   - Read the content.
   - Write a summarized answer with sources.

---

## 🧪 Testing

The backend includes a comprehensive test suite to verify logic and API connections.

```bash
cd backend
python comprehensive_test.py
```
This runs tests for:
- Factual queries
- Comparison queries
- Recent news
- Error handling

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User Interface] -->|POST /search| API[FastAPI Backend]
    API -->|Decompose| Planner[Grok (OpenRouter)]
    Planner -->|Sub-Queries| Search[Tavily Search API]
    Search -->|Parallel Requests| Web[Internet]
    Web -->|Raw Content| Search
    Search -->|Context| Synthesizer[Grok (OpenRouter)]
    Synthesizer -->|Final Answer| API
    API -->|JSON| User
```

## ⚠️ Known Limitations & Costs

- **Tavily Free Tier**: Limited to 1,000 searches/month.
- **OpenRouter**: Rate limits depend on the specific model and OpenRouter tier.
- **Latency**: Complex queries may take 10-20 seconds to ensure deep research.

## 🔧 Troubleshooting

**Error: `[Errno 10048] only one usage of each socket address...`**
- The backend is already running in another terminal. Close the other terminal or stop the process.

**Error: `404 Resource Not Found` (OpenRouter)**
- This usually means the model name in `llm.py` is incorrect or the model is not available on OpenRouter. Verify the model ID on OpenRouter.

**Error: `TAVILY_API_KEY not set`**
- Ensure your `.env` file is inside the `backend/` folder, not the root folder.

## License

MIT