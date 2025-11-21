import asyncio
import os
from agent import ResearchAgent
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("Testing ResearchAgent...")
    try:
        agent = ResearchAgent()
        query = "What is the difference between new graphics card and old graphics card of NVIDIA according to the latest news"
        print(f"Query: {query}")
        
        result = await agent.research(query)
        
        print("\n--- Result ---")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {len(result['sources'])}")
        for s in result['sources']:
            print(f"- {s['title']} ({s['url']})")
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
