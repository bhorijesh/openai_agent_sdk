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
    
    def run(self, outline: str, research: str, keywords: str , trend_summary: str , 
            tone: str , language: str , word_count: int ,intent: str , title: str ,
            blog_length: str = "medium", include_keywords: str = "", avoid_keywords: str = "",
            generated_title: str = "") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        # Use provided keywords or fallback to include_keywords
        final_keywords = keywords if keywords else include_keywords
        
        # Use provided title or generated_title
        blog_title = title if title else generated_title
            
        prompt = f"""
You are an expert AI blog writer specializing in product-focused content. Write a detailed product description blog using all keywords from {final_keywords} and incorporate trends from {trend_summary}. Follow the outline in {outline} *exactly* — do not skip, rename, merge, or reorder any H2 or H3 headings.

Blog Outline:
{outline}

Research Information:
{research}

Trend Summary:
{trend_summary}

Use H2 (`##`) for main titles and H3 (`###`) for subtopics. Maintain a consistent {tone} tone, write in {language}, and strictly match the {word_count} words (±5 words). Focus on detailed product specifications, problem-solving capabilities, and comprehensive product analysis for SEO optimization.

Structure:
- Begin with "## Introduction": one paragraph introducing the product-focused blog using {blog_title}. Do not insert a title here.
- For body content:
  - Use H2 for each main section from the outline.
  - Use H3 for each subsection from the outline.
  - Seamlessly integrate all keywords: {final_keywords} into the prose naturally.
  - Focus on detailed product descriptions, technical specifications, and how the product solves specific problems.
  - Use bullet points or numbered lists strictly when:
    - Highlighting product features or technical specifications
    - Detailing step-by-step product usage instructions
    - Enumerating product pros/cons, benefits, or technical tips
    - Presenting product comparison data or specification tables
  - Otherwise, structure subsections into two well-organized, detailed paragraphs with comprehensive product information.
- End with "## Conclusion": one paragraph summarizing the product benefits and key takeaways. Avoid generic opening phrases.

Parameters:
- Blog length: {blog_length}
- Include keywords: {final_keywords}
- Avoid keywords: {avoid_keywords}
- Intent: {intent}
- Target word count: {word_count} words

Important Guidelines:
1. Follow the outline structure exactly - do not add, remove, or modify headings
2. Incorporate research findings naturally throughout the content
3. Use trends from trend summary to make content current and relevant
4. Ensure all keywords are integrated seamlessly into the text
5. Maintain the specified tone and language throughout
6. Do not add content beyond what's outlined
7. Create clear, SEO-optimized, plagiarism-free content

Write the complete blog post.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Writer agent: {str(e)}]"
