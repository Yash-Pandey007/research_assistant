import asyncio
from agent import ResearchAgent
from dotenv import load_dotenv

load_dotenv()

async def test_single_question():
    agent = ResearchAgent()
    
    # Test a simple factual question
    query = "What is Python programming language?"
    print(f"\n{'='*80}")
    print(f"Testing: {query}")
    print(f"{'='*80}\n")
    
    try:
        result = await agent.research(query)
        
        print(f"\n{'='*80}")
        print("RESULTS")
        print(f"{'='*80}\n")
        print(f"Answer ({len(result['answer'])} chars):")
        print(result['answer'])
        print(f"\n\nSources ({len(result['sources'])}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n[{i}] {source['title']}")
            print(f"    {source['url']}")
            print(f"    Content preview: {source['content'][:100]}...")
        
        print(f"\n{'='*80}")
        if len(result['answer']) > 50 and len(result['sources']) > 0:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED - Insufficient results")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_single_question())
