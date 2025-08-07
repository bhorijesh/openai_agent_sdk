from .base import create_agent, call_openai_sync

class Proofreader:
    def __init__(self):
        """Initialize the Proofreader agent."""
        self.agent = create_agent(
            name="Professional Proofreader",
            instructions="""You are a professional proofreader specialized in grammar, spelling, clarity, and style improvements. 
            Your role is to review blog content and make final corrections to ensure it meets high editorial standards. 
            Focus on grammar, spelling, punctuation, sentence structure, clarity, flow, and overall readability while 
            preserving the author's voice and intent. Ensure the final output is polished and professional."""
        )
    
    def run(self, draft: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are a professional proofreader. Review the following blog post and make necessary corrections for grammar, spelling, clarity, and style. Provide the final, polished version.

Blog Post to Proofread:
{draft}

Please check and improve:
1. Grammar and sentence structure
2. Spelling and punctuation
3. Clarity and readability
4. Flow and transitions between paragraphs
5. Consistency in tone and style
6. Overall polish and professionalism

Provide the corrected and improved version:

Proofread Blog Post:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Proofreader agent: {str(e)}]"
