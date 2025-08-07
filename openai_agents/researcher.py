from .base import create_agent, call_openai_sync
from .web_search import web_search_tool
import logging

# Configure logging for researcher activities
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Researcher:
    def __init__(self):
        """Initialize the Researcher agent."""
        self.agent = create_agent(
            name="Research Assistant",
            instructions="""You are a helpful research assistant specialized in gathering comprehensive and accurate information. 
            Your role is to research blog topics in detail and provide concise summaries of the most important facts, 
            statistics, and insights. You have access to real-time web search data to provide current and accurate information.
            Focus on providing well-researched, factual content that would be valuable for creating high-quality blog posts.
            When provided with search results, analyze and synthesize the information to create comprehensive summaries."""
        )
        self.web_search = web_search_tool
    
    def run(self, topic: str, include_news: bool = True) -> str:
        """
        Research a topic using web search and provide comprehensive analysis.
        
        Args:
            topic (str): The topic to research
            include_news (bool): Whether to include recent news in the research
        
        Returns:
            str: Research summary with facts, statistics, and insights
        """
        if not self.agent:
            logger.error("❌ Researcher agent not initialized - missing OpenAI API key")
            return "[OpenAI API key missing]"
        
        logger.info(f"🎯 Starting research for topic: '{topic}' (include_news: {include_news})")
        
        # Perform web searches to gather current information
        search_results = []
        
        # General search for the topic
        logger.info("🔍 Performing general search...")
        general_results = self.web_search.search(f"{topic} facts statistics trends 2024 2025", num_results=8)
        search_results.extend(general_results)
        
        # Search for recent developments if requested
        if include_news:
            logger.info("📰 Performing news search...")
            news_results = self.web_search.search_news(f"{topic} latest developments news", num_results=5)
            search_results.extend(news_results)
        
        # Search for statistics and data
        logger.info("📊 Performing statistical data search...")
        stats_results = self.web_search.search(f"{topic} statistics data market research", num_results=5)
        search_results.extend(stats_results)
        
        logger.info(f"📋 Total search results collected: {len(search_results)}")
        
        # Format search results for the AI
        formatted_search_data = self.web_search.format_search_results(search_results)
        
        prompt = f"""
Research the following blog topic in detail using the provided current web search data and provide a concise summary of the most important facts, statistics, and insights:

Topic: {topic}

Current Web Search Data:
{formatted_search_data}

Based on the above search results and your knowledge, please provide:
1. Key facts and current information about this topic
2. Relevant statistics and data points (with sources when available)
3. Important insights and trends
4. Any notable developments or changes in this area
5. Current market status or recent news (if applicable)

Please synthesize the information from the search results and present it in a well-organized, comprehensive summary that would be valuable for creating a high-quality blog post. Cite specific data points and sources when possible.

Summary:
"""
        
        try:
            logger.info("🤖 Sending research data to OpenAI agent for analysis...")
            result = call_openai_sync(self.agent, prompt)
            logger.info("✅ Research completed successfully")
            
            # Print search statistics
            self.web_search.print_search_stats()
            
            return result
        except Exception as e:
            logger.error(f"❌ Error in Researcher agent: {str(e)}")
            return f"[Error in Researcher agent: {str(e)}]"
    
    def quick_research(self, topic: str) -> str:
        """
        Perform a quick research without news for faster results.
        
        Args:
            topic (str): The topic to research
        
        Returns:
            str: Quick research summary
        """
        logger.info(f"⚡ Starting quick research for topic: '{topic}'")
        return self.run(topic, include_news=False)
