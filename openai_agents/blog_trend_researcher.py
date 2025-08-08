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

    def run(self, topic: str, keywords_result: str, current_year: str = "2025", language: str = "English") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are a blog trend researcher for {current_year}, using the Serper tool to analyze trending content related to '{topic}' with relevant search terms based on '{keywords_result}'.
keyword: "{keywords_result}"

Follow these strict steps:
1. Execute a single, natural language query in Serper. Example:
   "Current trending blog topics about {keywords_result} in {current_year}"
2. Based on the search results:
   - Summarize the **most recent trending blog content**, focusing on emerging keywords, styles, and angles around '{keywords_result}'.
   - Identify the **most popular blog formats** (e.g., listicles, how-to guides, case studies, tutorials, or multimedia-heavy posts).
   - Highlight **key subtopics, content angles, and unique themes** that are dominating the space.
   - Keep the summary detailed, insightful, and actionable for SEO-driven blog planning.
3. Output the result in the following **precise JSON format** (with no extra formatting):

{{
  "summary": "Detailed paragraph summary based on search results covering trending content, top formats, and standout themes.",
  "blog_titles": [
    "Highly compelling, SEO-friendly blog titles using a keyword",
    "Another trending title with a keyword",
    "Outcome-focused blog with a keyword",
    "Solution-oriented  post featuring a keyword",
    "Transformation-focused using a keyword",
    "Value-driven content with a keyword"
  ]
}}

Important:
- Do not add any markdown, code formatting, or additional explanations.
- Ensure the JSON output is the **only output**.
- Craft each 'blog_title' to be highly compelling, SEO-friendly, and directly incorporate '{keywords_result}', aligned with trending styles for 2025 in {language} Language.

Expected Output:
{{
  "summary": "Detailed paragraph summary based on search results covering trending content, top formats, and standout themes.",
  "blog_titles": [
    "Highly compelling, SEO-friendly blog titles using a keyword",
    "Another trending title with a keyword",
    "Outcome-focused blog with a keyword",
    "Solution-oriented  post featuring a keyword",
    "Transformation-focused using a keyword",
    "Value-driven content with a keyword"
  ]
}}
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in BlogTrendResearcher agent: {str(e)}]"
