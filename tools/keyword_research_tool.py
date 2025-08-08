"""
Keyword Research Tool - Custom tool wrapper for GoogleKeywordIdeaGenerator
Specifically designed for the KeywordResearcher agent
"""

import os
from typing import List, Dict, Optional

# Import the Google Keyword Idea Generator
from .google import GoogleKeywordIdeaGenerator


class GoogleKeywordIdeaGeneratorTool:
    """
    Tool wrapper for GoogleKeywordIdeaGenerator specifically for keyword research.
    This tool integrates with the KeywordResearcher agent to provide Google Ads keyword data.
    """
    
    def __init__(self, location_id: str = "2840", page_size: int = 20):
        """
        Initialize the Google Keyword Idea Generator Tool.
        
        Args:
            location_id (str): Geographic location ID (default: 2840 for United States)
            page_size (int): Number of results per page (default: 20)
        """
        self.location_id = location_id
        self.page_size = page_size
        self.generator = None
    
    def generate_keyword_ideas(self, keywords: Optional[List[str]] = None, url: Optional[str] = None) -> List[Dict]:
        """
        Generate keyword ideas using Google Ads API.
        
        Args:
            keywords (List[str]): List of seed keywords
            url (str): Optional URL for keyword generation
            
        Returns:
            List[Dict]: List of keyword data with metrics
        """
        try:
            # Initialize the generator with provided parameters
            if keywords and isinstance(keywords, str):
                keywords = [keywords]
            
            self.generator = GoogleKeywordIdeaGenerator(
                location_id=self.location_id,
                keywords=keywords,
                url=url
            )
            
            # Set page size
            self.generator.set_page_size(self.page_size)
            
            # Get results
            results = self.generator.get_results()
            
            return results
            
        except Exception as e:
            return [{"error": f"Keyword generation failed: {str(e)}"}]
    
    def search_keywords(self, topic: str, seed_keywords: str = "") -> List[Dict]:
        """
        Search for keywords based on topic and seed keywords.
        Convenience method for the keyword researcher.
        
        Args:
            topic (str): Main topic for keyword research
            seed_keywords (str): Comma-separated seed keywords
            
        Returns:
            List[Dict]: List of keyword data
        """
        # Combine topic and seed keywords
        all_keywords = [topic]
        if seed_keywords:
            seed_list = [k.strip() for k in seed_keywords.split(",") if k.strip()]
            all_keywords.extend(seed_list)
        
        return self.generate_keyword_ideas(keywords=all_keywords)
    
    def get_keyword_metrics(self, keywords: List[str]) -> List[Dict]:
        """
        Get detailed metrics for specific keywords.
        
        Args:
            keywords (List[str]): List of keywords to analyze
            
        Returns:
            List[Dict]: Keyword metrics including competition, CPC, search volume
        """
        return self.generate_keyword_ideas(keywords=keywords)
    
    def format_for_researcher(self, results: List[Dict]) -> str:
        """
        Format results specifically for the KeywordResearcher agent.
        Returns only the text fields as requested.
        
        Args:
            results (List[Dict]): Raw keyword results
            
        Returns:
            str: Formatted bullet point list of keywords
        """
        if not results or (len(results) == 1 and "error" in results[0]):
            return "No keyword results available"
        
        # Extract only the 'text' field as requested by the researcher
        keywords = []
        for result in results:
            if "text" in result and result["text"]:
                keywords.append(f"• {result['text']}")
        
        return "\n".join(keywords[:15])  # Limit to 15 as requested
    
    def search_and_format(self, topic: str, seed_keywords: str = "") -> str:
        """
        Complete workflow: search keywords and format for researcher.
        
        Args:
            topic (str): Main topic
            seed_keywords (str): Seed keywords
            
        Returns:
            str: Formatted keyword list
        """
        results = self.search_keywords(topic, seed_keywords)
        return self.format_for_researcher(results)


# Convenience instance for easy import
keyword_tool = GoogleKeywordIdeaGeneratorTool()
