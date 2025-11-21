import os
import asyncio
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class SearchClient:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        self.client = TavilyClient(api_key=api_key)

    async def search(self, query: str, max_results: int = 5) -> list[dict]:
        print(f"Analyzing query: {query}")
        
        # Detect if query contains URLs
        if "http" in query.lower() or "www." in query.lower():
            return await self._use_extract(query)
        # Detect if query is about a specific website
        elif "site:" in query.lower() or "website" in query.lower():
            return await self._use_map(query)
        else:
            return await self._use_search(query, max_results)

    async def _use_search(self, query: str, max_results: int = 5) -> list[dict]:
        print(f"🔍 Using Tavily SEARCH for: {query}")
        try:
            # FIXED: Run blocking call in a thread
            response = await asyncio.to_thread(
                self.client.search,
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_raw_content=False,
                include_answer=False,
                include_images=False
            )
            
            results = response.get('results', [])
            return self._format_results(results)
            
        except Exception as e:
            print(f"❌ Tavily SEARCH error: {e}")
            return []

    async def _use_extract(self, query: str) -> list[dict]:
        print(f"📄 Using Tavily EXTRACT for: {query}")
        try:
            import re
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', query)
            
            if not urls:
                return await self._use_search(query)
            
            # FIXED: Run blocking call in a thread
            response = await asyncio.to_thread(self.client.extract, urls=urls)
            
            results = response.get('results', [])
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "url": result.get("url", ""),
                    "title": result.get("title", "Extracted Content"),
                    "content": result.get("raw_content", result.get("content", ""))
                })
            return formatted_results
            
        except Exception as e:
            print(f"❌ Tavily EXTRACT error: {e}")
            return []

    async def _use_map(self, query: str) -> list[dict]:
        # Mapping logic...
        # For simplicity, falling back to search logic here with site: param
        # but ensuring it's non-blocking
        return await self._use_search(query, max_results=5)

    def _format_results(self, results: list) -> list[dict]:
        formatted = []
        for result in results:
            formatted.append({
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "content": result.get("content", "")
            })
        return formatted