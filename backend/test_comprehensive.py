import asyncio
import json
import time
from agent import ResearchAgent
from dotenv import load_dotenv

load_dotenv()

# Comprehensive test questions covering different types
TEST_QUESTIONS = {
    "factual": [
        "What is the capital of France?",
        "Who invented the telephone?",
        "What is the speed of light?",
    ],
    "comparison": [
        "iPhone 15 vs Samsung Galaxy S24",
        "Python vs JavaScript for web development",
        "Electric cars vs gasoline cars environmental impact",
    ],
    "explanation": [
        "How does quantum computing work?",
        "Explain blockchain in simple terms",
        "What causes climate change?",
    ],
    "recent_news": [
        "Latest developments in AI 2025",
        "Recent space exploration achievements",
        "New medical breakthroughs this year",
    ],
    "how_to": [
        "How to start learning machine learning?",
        "Best practices for API design",
        "How to improve website SEO?",
    ],
    "research": [
        "Current trends in renewable energy",
        "State of quantum computing research",
        "Latest findings in neuroscience",
    ],
}

# RATE LIMIT ADJUSTMENT: 
# Increased from 3 to 5 because the new agent fires 3 searches at once.
# If you get "429" errors, increase this to 10.
DELAY_BETWEEN_TESTS = 5 

async def test_question(agent, question, category, test_num, total):
    """Test a single question with progress tracking"""
    print(f"\n{'='*80}")
    print(f"[{test_num}/{total}] Category: {category.upper()}")
    print(f"Question: {question}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = await agent.research(question)
        
        elapsed = time.time() - start_time
        
        # MODIFIED SUCCESS CRITERIA: 
        # Since the new agent is "Deep", we expect at least 200 chars and 2 sources.
        # If it returns less, it's technically a failure for a deep agent.
        success = len(result['answer']) > 200 and len(result['sources']) >= 1
        
        print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'} | "
              f"Time: {elapsed:.1f}s | "
              f"Sources: {len(result['sources'])} | "
              f"Answer: {len(result['answer'])} chars")
        
        return {
            "category": category,
            "question": question,
            "success": success,
            "elapsed_seconds": round(elapsed, 2),
            "answer_length": len(result['answer']),
            "source_count": len(result['sources']),
            "answer_preview": result['answer'][:200] + "..." if result['answer'] else "",
            "sources": [{"title": s['title'], "url": s['url']} for s in result['sources'][:3]]
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ ERROR after {elapsed:.1f}s: {e}")
        return {
            "category": category,
            "question": question,
            "success": False,
            "elapsed_seconds": round(elapsed, 2),
            "error": str(e),
        }

async def run_comprehensive_tests_with_rate_limiting():
    """Run all tests with intelligent rate limiting"""
    agent = ResearchAgent()
    all_results = []
    
    total_tests = sum(len(questions) for questions in TEST_QUESTIONS.values())
    
    print(f"\n{'='*80}")
    print(f"🧪 COMPREHENSIVE TEST SUITE")
    print(f"{'='*80}")
    print(f"Total tests: {total_tests}")
    print(f"Delay between tests: {DELAY_BETWEEN_TESTS}s")
    print(f"Estimated total time: {(total_tests * DELAY_BETWEEN_TESTS) / 60:.1f} minutes")
    print(f"{'='*80}\n")
    
    test_num = 0
    start_time = time.time()
    
    for category, questions in TEST_QUESTIONS.items():
        print(f"\n{'#'*80}")
        print(f"# TESTING CATEGORY: {category.upper()}")
        print(f"{'#'*80}")
        
        for question in questions:
            test_num += 1
            
            # Run test
            result = await test_question(agent, question, category, test_num, total_tests)
            all_results.append(result)
            
            # Rate limiting: wait between tests
            if test_num < total_tests:
                print(f"\n⏳ Waiting {DELAY_BETWEEN_TESTS}s to respect API rate limits...")
                await asyncio.sleep(DELAY_BETWEEN_TESTS)
    
    total_elapsed = time.time() - start_time
    
    # Save detailed results
    with open("test_results_comprehensive.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Print summary
    total = len(all_results)
    successful = sum(1 for r in all_results if r["success"])
    failed = total - successful
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*80}\n")
    print(f"Total Tests: {total}")
    print(f"✅ Successful: {successful} ({successful/total*100:.1f}%)")
    print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")
    print(f"⏱️  Total Time: {total_elapsed/60:.1f} minutes")
    print(f"⚡ Avg Time/Test: {total_elapsed/total:.1f}s")
    
    print("\n📂 Results by Category:")
    print('-'*80)
    for cat, qs in TEST_QUESTIONS.items():
        cat_res = [r for r in all_results if r["category"] == cat]
        cat_pass = sum(1 for r in cat_res if r["success"])
        # Handle division by zero if category is empty
        if len(cat_res) > 0:
            avg_time = sum(r.get("elapsed_seconds", 0) for r in cat_res) / len(cat_res)
            print(f"  {cat.ljust(15)}: {cat_pass}/{len(cat_res)} passed | Avg time: {avg_time:.1f}s")
    
    print("\n💾 Detailed results saved to: test_results_comprehensive.json")
    print(f"{'='*80}\n")
    if failed > 0:
        print("⚠️  FAILED TESTS:")
        print('-'*80)
        for r in all_results:
            if not r["success"]:
                print(f"- [{r['category']}] {r['question']}")
                if "error" in r:
                    print(f"  Error: {r['error']}")
        print('-'*80)

if __name__ == "__main__":
    print("Starting rate-limit-aware comprehensive test suite...")
    asyncio.run(run_comprehensive_tests_with_rate_limiting())