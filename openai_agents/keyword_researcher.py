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
    
    def generate_seed_keywords(self, topic: str, tone: str = "professional", language: str = "English") -> str:
        """Generate initial seed keywords for the topic."""
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
Analyze the provided {topic} and generate an initial set of relevant seed keywords.
These keywords should be closely related to the {topic} and suitable for further keyword expansion.
Consider the specified {tone} and {language} to ensure contextual relevance.
Output only the generated seed keywords as a bullet point list, with no extra commentary or formatting.

Expected Output:
Provide a clean list of 5 seed keywords or keyphrases directly related to the {topic}.
Format your response as a bullet point list with no additional explanation or transformation.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in KeywordResearcher seed generation: {str(e)}]"
    
    def run(self, topic: str, keyword: str = "", tone: str = "professional", language: str = "English") -> str:
        """Execute comprehensive keyword research."""
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
Execute comprehensive keyword research to support SEO strategy for a blog post related to the {topic} and the provided seed keywords {keyword}.
These keywords stem from detailed product information including features, specifications, and benefits.
Consider the user's specified tone ({tone}) and language ({language}) for contextual relevance.
Utilize the custom GoogleKeywordIdeaGeneratorTool with {topic} and {keyword} as keywords to extract raw keyword ideas.   
Your task is strictly to extract keywords from the tool's output without modification.

Expected Output:
Provide a clean list of 10-15 SEO-friendly keyword suggestions or keyphrases.
Output only the 'text' fields exactly as returned by the keyword generation tool.
Format your response as a bullet point list with no additional commentary, explanation, or transformation.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in KeywordResearcher agent: {str(e)}]"
