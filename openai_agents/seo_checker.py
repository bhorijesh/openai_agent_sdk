from .base import create_agent, call_openai_sync

class SEOChecker:
    def __init__(self):
        """Initialize the SEOChecker agent."""
        self.agent = create_agent(
            name="SEO Optimization Expert",
            instructions="""You are an SEO expert specialized in optimizing content for search engines while maintaining readability and user engagement. 
            Your role is to review blog content and suggest improvements that will help it rank better in search results. 
            Focus on keyword optimization, content structure, readability, and technical SEO elements while ensuring 
            the content remains natural and valuable for human readers."""
        )
    
    def run(self, draft: str, keywords: str) -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are an SEO expert. Review the following blog draft and optimize it for the given keywords while maintaining readability and engagement.

Blog Draft:
{draft}

Target Keywords:
{keywords}

Please provide an improved version of the blog post that includes:

1. **SEO Optimizations Made:**
   - Keyword integration improvements
   - Title and heading optimizations
   - Meta description suggestion
   - Internal linking opportunities
   - Content structure improvements

2. **Optimized Blog Post:**
   - Improved version with better keyword integration
   - Enhanced headings and subheadings
   - Better content flow and structure
   - Maintained natural language and readability
   - Added meta description at the end

Make sure to:
- Integrate keywords naturally without keyword stuffing
- Optimize headings (H1, H2, H3) for SEO
- Improve content structure for better readability
- Suggest internal linking opportunities
- Maintain the engaging tone and valuable content

SEO Analysis and Improved Blog Post:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in SEOChecker agent: {str(e)}]"
