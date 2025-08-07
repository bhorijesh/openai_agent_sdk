from .base import create_agent, call_openai_sync

class Writer:
    def __init__(self):
        """Initialize the Writer agent."""
        self.agent = create_agent(
            name="Professional Blog Writer",
            instructions="""You are a professional blog writer specialized in creating engaging and informative content. 
            Your role is to transform outlines and research into compelling, well-written blog posts that engage readers 
            and provide valuable information. Use a friendly, engaging tone while maintaining professionalism. 
            Focus on creating content that is both informative and enjoyable to read, with clear structure and smooth flow."""
        )
    
    def run(self, outline: str, research: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are a professional blog writer. Write a comprehensive, engaging blog post based on the following outline and research. 

Blog Outline:
{outline}

Research Information:
{research}

Instructions for writing:
1. Use a friendly, engaging tone that connects with readers
2. Expand each section from the outline into detailed, informative paragraphs
3. Incorporate the research findings naturally throughout the content
4. Use clear, readable language that's accessible to a broad audience
5. Include smooth transitions between sections
6. Make the content actionable and valuable for readers
7. Aim for approximately 1000-1500 words
8. Use subheadings to break up the content and improve readability

Write the complete blog post now:

Blog Post:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Writer agent: {str(e)}]"
