import asyncio
import json
from agent import ResearchAgent
from dotenv import load_dotenv

load_dotenv()

TEST_QUESTIONS = [
    # Phase 1: Ideation
    "What are the current major debates or controversies in the field of Quantum Computing?",
    
    # Phase 2: Literature Review (Simulated)
    "What are the standard seminal papers or authors associated with Deep Learning?",
    
    # Phase 3: Understanding Complex Concepts
    "Explain the concept of CRISPR to me as if I were a 12-year-old.",
    
    # Phase 4: Methodology
    "What are the pros and cons of using a Case Study vs. Survey for social science research?",
    
    # Phase 5: Writing (Logic check)
    "Suggest a catchy but professional title for a paper about the impact of AI on software engineering jobs."
]

async def run_tests():
    agent = ResearchAgent()
    results = []
    
    print(f"Starting comprehensive test with {len(TEST_QUESTIONS)} questions...")
    
    for i, question in enumerate(TEST_QUESTIONS):
        print(f"\n[{i+1}/{len(TEST_QUESTIONS)}] Testing: {question}")
        try:
            result = await agent.research(question)
            
            # Basic validation
            has_answer = len(result['answer']) > 50
            has_sources = len(result['sources']) > 0
            
            print(f"  -> Answer Length: {len(result['answer'])} chars")
            print(f"  -> Sources Found: {len(result['sources'])}")
            
            results.append({
                "question": question,
                "success": has_answer,
                "answer_snippet": result['answer'][:200] + "...",
                "source_count": len(result['sources'])
            })
            
        except Exception as e:
            print(f"  -> ERROR: {e}")
            results.append({
                "question": question,
                "success": False,
                "error": str(e)
            })
            
    # Save report
    with open("test_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nTest complete. Results saved to test_report.json")

if __name__ == "__main__":
    asyncio.run(run_tests())
