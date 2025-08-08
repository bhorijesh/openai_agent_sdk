import os
import json
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


def orchestrate_blog_creation(config: Dict[str, Any]) -> Dict[str, Any]:
    # Initialize all specialized agents
    researcher = Researcher()
    keyworder = KeywordResearcher()
    trender = BlogTrendResearcher()
    outliner = OutlineCreator()
    writer = Writer()
    seo = SEOChecker()
    proofreader = Proofreader()

    # Extract values from config
    topic = config.get("topic", "")
    keywords = config.get("keywords", "")
    tone = config.get("tone", "professional")
    language = config.get("language", "English")
    current_year = config.get("current_year", "2025")
    audience = config.get("audience", "general")
    word_count = config.get("word_count", 1200)
    blog_length = config.get("blog_length", "medium")
    include_keywords = config.get("include_keywords", "")
    avoid_keywords = config.get("avoid_keywords", "")
    intent = config.get("intent", "inform")
    title = config.get("title", "")
    url = config.get("url", "")
    generated_title = config.get("generated_title", "")

    # Execute the sequential workflow with each specialized agent
    print(f"Researching topic: {topic}")
    research = researcher.run(topic, keywords)
    seed_keywords = keyworder.generate_seed_keywords(topic, tone, language)
    keywords_result = keyworder.run(topic, seed_keywords, tone, language)
    trends = trender.run(topic, keywords_result, current_year, language)
    trend_summary = ""
    trending_titles = []
    
    if isinstance(trends, str):
        try:
            trends_data = json.loads(trends)
            trend_summary = trends_data.get("summary", "")
            trending_titles = trends_data.get("blog_titles", [])
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            trend_summary = trends  
    else:
        trend_summary = trends.get("summary", str(trends)) if isinstance(trends, dict) else str(trends)
    print(f"Trend summary: {trend_summary}")
    outline = outliner.run(keywords_result, topic, research, trend_summary)
 
    draft = writer.run(
        outline=outline, 
        research=research, 
        keywords=keywords_result, 
        trend_summary=trend_summary,
        tone=tone, 
        language=language, 
        word_count=word_count,
        blog_length=blog_length, 
        include_keywords=include_keywords, 
        avoid_keywords=avoid_keywords,
        intent=intent, 
        title=topic, 
        generated_title=generated_title
    )

    
    seo_result = seo.run(draft, keywords_result)
    final_blog = proofreader.run(draft, word_count, audience, url)
    
    # Save to MD file
    os.makedirs("output", exist_ok=True)
    filename = f"output/blog_{topic.replace(' ', '_')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {topic}\n\n{final_blog}")
    
    return {
        "final_blog": final_blog,

    }
