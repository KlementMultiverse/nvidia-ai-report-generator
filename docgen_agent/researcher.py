from typing import TypedDict, List, Literal
from langchain_core.messages import HumanMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM — NVIDIA NIM (FREE)
llm = ChatNVIDIA(
    model="meta/llama3-8b-instruct",  # Free, fast, powerful
    api_key=os.getenv("NGC_API_KEY"),
    temperature=0.1
)

# Initialize Tavily (FREE)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Tool function
def search_tavily(queries: List[str], topic: Literal["general", "news", "finance"] = "general") -> str:
    """Search the web using Tavily API"""
    results = []
    for query in queries:
        try:
            response = tavily_client.search(query, max_results=3, topic=topic)
            for result in response.get('results', []):
                results.append(f"URL: {result['url']}\nContent: {result['content'][:300]}...")
        except Exception as e:
            results.append(f"Search failed for '{query}': {str(e)}")
    return "\n\n".join(results)

# Research prompt (from NVIDIA blog)
RESEARCH_PROMPT_TEMPLATE = """
Your goal is to generate 3 targeted web search queries to gather comprehensive information for writing a technical report section.

Topic: {topic}

Queries should:
1. Cover different aspects (technical, applications, trends)
2. Include specific terms + year (e.g., "2025")
3. Target authoritative sources (docs, papers, case studies)

Return ONLY the 3 queries — one per line.
"""

async def researcher_node(topic: str) -> str:
    """Simple ReAct: Generate queries → Search → Return results"""
    # Step 1: Generate queries
    prompt = RESEARCH_PROMPT_TEMPLATE.format(topic=topic)
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    queries_text = response.content.strip()
    queries = [q.strip() for q in queries_text.split("\n") if q.strip()]

    # Step 2: Execute search
    print(f"🔍 Generated queries: {queries}")
    search_result = search_tavily(queries, "general")
    
    return search_result
