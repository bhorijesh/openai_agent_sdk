from .base import create_agent, call_openai_sync

class OutlineCreator:
    def __init__(self):
        """Initialize the OutlineCreator agent."""
        self.agent = create_agent(
            name="Blog Outline Creator",
            instructions="""You are a blog outline creator specialized in structuring content in a logical and engaging manner. 
            Your role is to create detailed, well-organized outlines for blog posts that flow logically and engage readers. 
            You should incorporate research findings, SEO keywords naturally, and trending angles to create comprehensive outlines 
            that serve as excellent blueprints for high-quality blog content."""
        )
    
    def run(self, research: str, keywords: str, trends: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are a blog outline creator. Using the following research, keywords, and trends, create a detailed outline for a comprehensive blog post.

Research Findings:
{research}

SEO Keywords:
{keywords}

Current Trends:
{trends}

Please create a detailed blog outline that includes:

1. **Introduction** (Hook, problem statement, what readers will learn)
2. **4-6 Main Sections** with:
   - Clear headings that incorporate keywords naturally
   - 2-3 subpoints for each section
   - Integration of trending angles where relevant
3. **Conclusion** (Summary, call-to-action, next steps)

Make sure the outline:
- Flows logically from introduction to conclusion
- Incorporates the research findings naturally
- Uses SEO keywords in headings where appropriate
- Reflects current trends to make content timely and engaging
- Provides clear value to readers

Blog Outline:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in OutlineCreator agent: {str(e)}]"
