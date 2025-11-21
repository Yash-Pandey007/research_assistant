from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ResearchAgent
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent once on startup
agent = ResearchAgent()

class SearchRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"status": "Backend is running", "message": "Use /search endpoint"}

@app.post("/search")
async def search(request: SearchRequest):
    print(f"Incoming request: {request.query}")
    try:
        result = await agent.research(request.query)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc() # Print error to console
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)