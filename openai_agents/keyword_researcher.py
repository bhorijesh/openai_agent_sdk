from .base import create_agent, call_openai_sync

class KeywordResearcher:
    def __init__(self):
        """Initialize the KeywordResearcher agent."""
        self.agent = create_agent(
            name="SEO Keyword Expert",
            instructions="""You are an expert in SEO and keyword research specialized in finding relevant keywords for content optimization. 
            Your role is to identify the most effective keywords and key phrases that will help content rank well in search engines. 
            Focus on providing comprehensive keyword lists that include primary keywords, long-tail keywords, and related terms 
            that are relevant to the given topic."""
        )
    
    def run(self, topic: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are an expert in SEO and keyword research. Analyze the following blog topic and provide the top 10 most relevant keywords and key phrases that would help this content rank well in search engines.

Topic: {topic}

Please provide:
1. Primary keywords (1-3 main keywords)
2. Long-tail keywords (3-4 phrases)
3. Related and semantic keywords (3-4 terms)

Present them as a comma-separated list, starting with the most important keywords first.

Keywords:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in KeywordResearcher agent: {str(e)}]"
