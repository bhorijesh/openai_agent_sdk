from .base import create_agent, call_openai_sync

class Researcher:
    def __init__(self):
        """Initialize the Researcher agent."""
        self.agent = create_agent(
            name="Research Assistant",
            instructions="""You are a helpful research assistant specialized in gathering comprehensive and accurate information. 
            Your role is to research blog topics in detail and provide concise summaries of the most important facts, 
            statistics, and insights. Focus on providing well-researched, factual content that would be valuable for 
            creating high-quality blog posts."""
        )
    
    def run(self, topic: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
Research the following blog topic in detail and provide a concise summary of the most important facts, statistics, and insights:

Topic: {topic}

Please provide:
1. Key facts and current information about this topic
2. Relevant statistics and data points
3. Important insights and trends
4. Any notable developments or changes in this area

Summary:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Researcher agent: {str(e)}]"
