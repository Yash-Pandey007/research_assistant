from agent import ResearchAgent
import asyncio

async def test():
    agent = ResearchAgent()
    query = "I am interested in AI. Can you suggest 5 potential research questions that have not been extensively explored?"
    print(f"Testing query: {query}")
    result = await agent.research(query)
    print(f"\nSources found: {len(result['sources'])}")
    print(f"Answer length: {len(result['answer'])} chars")
    if result['sources']:
        print("\nFirst source:")
        print(f"  Title: {result['sources'][0]['title']}")
        print(f"  URL: {result['sources'][0]['url']}")
    else:
        print("\nNo sources found!")

asyncio.run(test())
