from .base import create_agent, call_openai_sync
from tools.keyword_research_tool import keyword_tool

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
        self.keyword_tool = keyword_tool
    
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
        
        # Use the Google Keyword Tool to get actual keyword data
        try:
            # Get keyword ideas from Google Ads API
            keyword_results = self.keyword_tool.search_and_format(topic, keyword)
            
            # If we got results from the tool, format them properly
            if keyword_results and keyword_results != "No keyword results available":
                prompt = f"""
Based on the keyword research for {topic} with seed keywords {keyword}, here are the raw keyword suggestions from Google Ads API:

{keyword_results}

Your task is to analyze these keywords and provide the final curated list of 10-15 SEO-friendly keywords.
Consider the user's specified tone ({tone}) and language ({language}) for contextual relevance.
Focus on keywords that are most relevant for blog content creation.

Expected Output:
Provide a clean list of 10-15 SEO-friendly keyword suggestions or keyphrases.
Format your response as a bullet point list with no additional commentary, explanation, or transformation.
Select the most relevant keywords from the provided list above.
"""
            else:
                # Fallback to AI-generated keywords if tool fails
                prompt = f"""
Execute comprehensive keyword research to support SEO strategy for a blog post related to the {topic} and the provided seed keywords {keyword}.
Consider the user's specified tone ({tone}) and language ({language}) for contextual relevance.
Note: Google Ads API data is currently unavailable, so generate research-based keyword suggestions.

Expected Output:
Provide a clean list of 10-15 SEO-friendly keyword suggestions or keyphrases.
Format your response as a bullet point list with no additional commentary, explanation, or transformation.
"""
        
        except Exception as tool_error:
            print(f"⚠️ Keyword tool error: {str(tool_error)}, falling back to AI generation")
            # Fallback prompt if tool fails
            prompt = f"""
Execute comprehensive keyword research to support SEO strategy for a blog post related to the {topic} and the provided seed keywords {keyword}.
Consider the user's specified tone ({tone}) and language ({language}) for contextual relevance.

Expected Output:
Provide a clean list of 10-15 SEO-friendly keyword suggestions or keyphrases.
Format your response as a bullet point list with no additional commentary, explanation, or transformation.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in KeywordResearcher agent: {str(e)}]"
