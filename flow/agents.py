import os
from typing import Any, Dict
from datetime import datetime

# Import all agents from the agents package
from openai_agents.researcher import Researcher
from openai_agents.keyword_researcher import KeywordResearcher
from openai_agents.blog_trend_researcher import BlogTrendResearcher
from openai_agents.outline_creator import OutlineCreator
from openai_agents.writer import Writer
from openai_agents.seo_checker import SEOChecker
from openai_agents.proofreader import Proofreader

def save_final_blog_md(final_blog: str, topic: str, filename: str = None) -> str:
    """Save final blog to Markdown file in the 'output' folder."""
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    if filename is None:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')[:30]  
        filename = f"blog_{safe_topic}_{timestamp}.md"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as mdfile:
        mdfile.write(f"# {topic}\n\n")
        mdfile.write(final_blog)
    
    return filepath

def orchestrate_blog_creation(topic: str) -> Dict[str, Any]:
    """
    Coordinate the workflow between all specialized OpenAI agents.
    
    This function orchestrates a multi-agent workflow where each agent has a specific role:
    1. Researcher Agent - Gathers comprehensive information
    2. Keyword Researcher Agent - Identifies SEO-relevant keywords
    3. Blog Trend Researcher Agent - Analyzes current trends
    4. Outline Creator Agent - Structures the content logically
    5. Writer Agent - Creates engaging content
    6. SEO Checker Agent - Optimizes for search engines
    7. Proofreader Agent - Ensures quality and polish
    """
    # Initialize all specialized agents
    researcher = Researcher()
    keyworder = KeywordResearcher()
    trender = BlogTrendResearcher()
    outliner = OutlineCreator()
    writer = Writer()
    seo = SEOChecker()
    proofreader = Proofreader()

    # Execute the sequential workflow with each specialized agent
    print(f"Researching topic: {topic}")
    research = researcher.run(topic)
    
    print("Finding relevant keywords...")
    keywords = keyworder.run(topic)
    
    print("Analyzing current trends...")
    trends = trender.run(topic)
    
    print("Creating content outline...")
    outline = outliner.run(research, keywords, trends)
    
    print("Writing blog content...")
    draft = writer.run(outline, research)
    
    print("Optimizing for SEO...")
    seo_result = seo.run(draft, keywords)
    
    print("Final proofreading...")
    final_blog = proofreader.run(seo_result)

    # Save only the final blog to Markdown
    md_filename = save_final_blog_md(final_blog, topic)
    
    print(f"Blog creation complete! Saved to: {md_filename}")
    
    # Return only the final blog and filename
    return {
        "final_blog": final_blog,
        "saved_file": md_filename
    }

if __name__ == "__main__":
    # If this file is run directly, provide a simple test
    test_topic = "The Benefits of Remote Work"
    result = orchestrate_blog_creation(test_topic)
