import asyncio
from llm import LLMClient
from search import SearchClient

class ResearchAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.search_client = SearchClient()

    async def research(self, user_query: str) -> dict:
        # 1. Decompose into Semantic Sub-Questions (Fix #1: Better Decomp)
        search_queries = await self._decompose_query(user_query)
        print(f"Researching sub-topics: {search_queries}")

        # 2. Execute Searches in PARALLEL (Fix #2: Speed)
        # Instead of waiting one by one, we fire all requests at once
        search_tasks = [self.search_client.search(query) for query in search_queries]
        results_list = await asyncio.gather(*search_tasks)
        
        # Flatten the list of lists (results_list comes back as [[res1, res2], [res3, res4]])
        search_results = [item for sublist in results_list for item in sublist]
        
        # Deduplicate results based on URL
        unique_results = {r['url']: r for r in search_results}.values()
        
        # 3. Synthesize Answer
        answer = await self._synthesize_answer(user_query, list(unique_results))
        
        return {
            "answer": answer,
            "sources": list(unique_results)
        }

    async def _decompose_query(self, user_query: str) -> list[str]:
        # FIX #3: Changed prompt to ask for "Questions" not "Keywords"
        # This helps retrieve articles that answer specific aspects of the topic
        prompt = f"""
        You are an expert research planner. The user has asked a complex question. 
        Break this down into 3 specific, distinct SUB-QUESTIONS that cover different angles of the topic.
        
        GUIDELINES:
        - Do NOT generate SEO keywords. Generate full, natural language questions.
        - Ensure the questions cover different aspects (e.g., economic, technical, historical).
        
        Example for "AI in Healthcare":
        1. What are the specific applications of AI in diagnostic radiology?
        2. What are the privacy concerns regarding patient data in AI systems?
        3. How does AI impact healthcare workforce employment statistics?
        
        User Question: {user_query}
        
        Return ONLY the 3 sub-questions, one per line.
        """
        response = await self.llm.generate_text(prompt)
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        
        if not queries:
            return [user_query]
        return queries[:3]

    async def _synthesize_answer(self, user_query: str, search_results: list[dict]) -> str:
        if not search_results:
            return "I couldn't find any relevant sources."
        
        # Sort results by length (assuming longer content = more depth)
        sorted_results = sorted(search_results, key=lambda x: len(x.get('content', '')), reverse=True)
        
        context = ""
        for i, result in enumerate(sorted_results[:7]): # Increased from default to top 7
            # FIX #4: Increased context limit from 500 to 4000 chars
            # 500 chars is just a headline. 4000 allows the LLM to read the actual article.
            content = result.get('content', '')[:4000]
            context += f"Source {i+1}: {result['title']}\nURL: {result['url']}\nContent: {content}\n\n"
            
        prompt = f"""
        You are a senior research analyst. Provide a comprehensive answer to the user's question based on the provided sources.
        
        User Question: {user_query}
        
        Available Sources:
        {context}
        
        Instructions:
        - Synthesize the data; do not just list summaries.
        - If the topic is complex, break your answer down into sections with headers.
        - Cite specific sources using [Source N] notation.
        - If sources disagree, explicitly mention the conflict.
        
        Your Answer:
        """
        
        answer = await self.llm.generate_text(prompt)
        return answer