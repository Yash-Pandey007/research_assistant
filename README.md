# Research Assistant

A web-based research assistant that answers questions by searching the web and synthesizing findings using an LLM.

## Features

✅ **Query Decomposition**: Breaks down complex questions into targeted search queries  
✅ **Web Search**: Uses Tavily API (purpose-built for AI/RAG)  
✅ **Content Extraction**: Automatic extraction with Tavily (no scraping needed!)  
✅ **LLM Synthesis**: Uses Google AI (Gemini 2.5 Pro) to synthesize answers  
✅ **Source Citations**: Properly cites all sources with URLs  
✅ **Deep Search Mode**: Adds delays between queries to avoid rate limits  
✅ **Insufficient Information Handling**: Clearly states when information is unavailable  

## Tech Stack

### Backend
- **FastAPI**: REST API
- **Google Generative AI**: LLM (Gemini 2.5 Pro)
- **Tavily API**: AI-optimized search with automatic content extraction
- **Python 3.x**

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **Tailwind CSS v4**: Styling

## Setup

### Backend

1. **Get API Keys:**
   - **Google AI**: Get free key at [ai.google.dev](https://ai.google.dev/)
   - **Tavily**: Sign up at [tavily.com](https://tavily.com/) (100 free searches/month)

2. Navigate to backend directory:
   ```bash
   cd backend
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=tvly-your_tavily_api_key_here
   ```

5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   Backend runs at: `http://localhost:8000`

### Frontend

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```
   Frontend runs at: `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Enter your question in the search box
3. Click "Search" or press Enter
4. Wait 15-30 seconds for deep search to complete
5. View the synthesized answer and sources

### Example Questions

- **"What is Python programming language?"**
- **"Latest developments in quantum computing"**
- **"Benefits of meditation"**
- **"Compare iPhone 15 and Pixel 8"**
- **"Explain blockchain in simple terms"**

## Tavily Features Used

This implementation uses all three Tavily functions:

1. **Search**: Main search with automatic content extraction
2. **Extract**: Extract content from specific URLs
3. **Crawl**: Crawl websites for comprehensive content

## Testing

Run the comprehensive test suite:
```bash
cd backend
python comprehensive_test.py
```

## API Endpoints

### `POST /search`
Perform a research query.

**Request:**
```json
{
  "query": "Your question here"
}
```

**Response:**
```json
{
  "answer": "Synthesized answer with citations...",
  "sources": [
    {
      "url": "https://example.com",
      "title": "Page Title",
      "content": "Extracted content..."
    }
  ]
}
```

### `GET /health`
Health check endpoint.

## Architecture

```
User Question
    ↓
Query Decomposition (Gemini 2.5 Pro)
    ↓
Generate 2-3 Search Queries
    ↓
Tavily Search (per query with 3s delay)
    ↓
Automatic Content Extraction (Tavily)
    ↓
Synthesize Answer (Gemini 2.5 Pro)
    ↓
Return Answer + Sources
```

## Cost

- **Google AI**: Free tier (60 requests/minute for Gemini 2.5 Pro)
- **Tavily**: 100 free searches/month, then $0.50 per 1000 searches

## Known Limitations

1. **Search Limits**: Tavily free tier = 100 searches/month
2. **Response Time**: 15-30 seconds per query (3 searches × 3s delay + processing)
3. **Query Quality**: Complex abstract queries may not find relevant results

## Troubleshooting

**"TAVILY_API_KEY environment variable not set" error:**
1. Sign up at tavily.com
2. Get your API key
3. Add it to `.env` file

**Empty answers:**
- Check that both API keys are valid
- Verify you haven't exceeded Tavily's monthly limit
- Check backend logs for errors

## License

MIT
