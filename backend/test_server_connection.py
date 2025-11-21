import asyncio
import uvicorn
import httpx
from main import app
import threading
import time

# Function to run the server in a separate thread
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001) # Use a different port to avoid conflicts

async def test_server():
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    async with httpx.AsyncClient() as client:
        try:
            # Test Health
            print("Testing /health endpoint...")
            response = await client.get("http://127.0.0.1:8001/health")
            print(f"Health Status: {response.status_code}")
            if response.status_code != 200:
                print("❌ Health check failed")
                return

            # Test Search (Simple query to avoid long wait/cost, but enough to trigger agent)
            # Note: This will actually call the LLM, so it costs money/credits. 
            # We'll use a very simple query.
            print("Testing /search endpoint...")
            response = await client.post(
                "http://127.0.0.1:8001/search", 
                json={"query": "What is 2+2? Answer briefly."}
            )
            print(f"Search Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if "answer" in data and "sources" in data:
                    print("✅ Server integration test passed!")
                    print(f"Answer: {data['answer'][:100]}...")
                else:
                    print("❌ Invalid response format")
            else:
                print(f"❌ Search failed: {response.text}")

        except Exception as e:
            print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_server())
