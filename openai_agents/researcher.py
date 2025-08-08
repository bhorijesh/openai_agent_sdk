from .base import create_agent, call_openai_sync
from tools.web_search_tool import WebSearchTool

class Researcher:
    def __init__(self):
        """Initialize the Researcher agent."""
        self.web_search = WebSearchTool()
        self.agent = create_agent(
            name="Research Assistant",
            instructions="""You are a helpful research assistant specialized in gathering comprehensive and accurate information. 
            Your role is to research blog topics in detail and provide concise summaries of the most important facts, 
            statistics, and insights. Focus on providing well-researched, factual content that would be valuable for 
            creating high-quality blog posts."""
        )
    
    def run(self, topic: str, keywords: str = "") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
        
        # Perform web searches to gather current information
        search_queries = [
            f"{topic} {keywords}",
            f"{topic} latest trends 2025",
            f"{topic} statistics data",
            f"{topic} industry insights"
        ]
        
        search_results = []
        for query in search_queries:
            results = self.web_search.search(query.strip(), num_results=3)
            if results and not (len(results) == 1 and 'error' in results[0]):
                search_results.extend(results)
        
        # Also search for recent news
        news_results = self.web_search.search_news(f"{topic} {keywords}".strip(), num_results=3)
        if news_results and not (len(news_results) == 1 and 'error' in news_results[0]):
            search_results.extend(news_results)
        
        # Format search results for the AI
        formatted_search_data = self.web_search.format_search_results(search_results)
        
        prompt = f"""
Based on the following real-time search data, perform a detailed and systematic research investigation on the topic '{topic}', emphasizing the keywords: {keywords}.

SEARCH DATA:
{formatted_search_data}

Using this current information from credible sources, organize your findings in a clear, logical structure with distinct sections covering:
  1. An introduction and overview of the topic
  2. Key insights and significant patterns discovered
  3. Emerging or related trends and developments
  4. Relevant data, statistics, or examples to support your findings
  5. Any notable controversies, challenges, or gaps in the topic

Expected Output:
Provide a structured research summary in a single, continuous paragraph that introduces the context and scope of the topic, presents main insights and key information discovered during the research, highlights emerging trends and developments, includes supporting evidence such as data points or cited sources when applicable, and notes controversies, challenges, or gaps in the topic. Use clear and concise language suitable for both technical and non-technical audiences.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Researcher agent: {str(e)}]"
