from .base import create_agent, call_openai_sync

class BlogTrendResearcher:
    def __init__(self):
        """Initialize the BlogTrendResearcher agent."""
        self.agent = create_agent(
            name="Blog Trend Analyst",
            instructions="""You are a blog trend analyst specialized in identifying current trends and popular angles for content creation. 
            Your role is to analyze what's currently trending in various industries and identify angles, hooks, or perspectives 
            that would make content more engaging and relevant to current audiences. Focus on providing actionable insights 
            about trending approaches that can make blog content more compelling and timely."""
        )
    
    def run(self, topic: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are a blog trend analyst. Analyze the following blog topic and identify current trends, angles, or hooks that are popular and would make this content more engaging and relevant.

Topic: {topic}

Please provide 3 trending approaches or perspectives that could make this blog post more compelling:

1. Current trend #1: [Describe the trend and how it relates to the topic]
2. Current trend #2: [Describe another trending angle]
3. Current trend #3: [Describe a third trending perspective]

For each trend, explain:
- What makes it currently relevant
- How it can be applied to this topic
- Why it would engage readers

Trends:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in BlogTrendResearcher agent: {str(e)}]"
