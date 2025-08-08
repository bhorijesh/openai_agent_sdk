import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class WebSearchTool:
    """Web search tool using Serper API for real-time information retrieval."""
    
    def __init__(self):
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.base_url = "https://google.serper.dev/search"
        self.search_count = 0
        self.last_search_time = None
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search the web using Serper API.
        
        Args:
            query (str): The search query
            num_results (int): Number of search results to return (default: 5)
            
        Returns:
            List[Dict]: List of search results with title, link, snippet
        """
        # Track search attempt
        self.search_count += 1
        self.last_search_time = datetime.now()
        
        if not self.serper_api_key:
            return [{"error": "SERPER_API_KEY not found in environment variables"}]
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Extract organic search results
            if 'organic' in data:
                organic_count = len(data['organic'][:num_results])
                for result in data['organic'][:num_results]:
                    results.append({
                        'title': result.get('title', ''),
                        'link': result.get('link', ''),
                        'snippet': result.get('snippet', ''),
                        'date': result.get('date', '')
                    })
            
            # Add answer box if available
            if 'answerBox' in data:
                answer_box = data['answerBox']
                results.insert(0, {
                    'title': 'Answer Box',
                    'link': answer_box.get('link', ''),
                    'snippet': answer_box.get('answer', answer_box.get('snippet', '')),
                    'date': '',
                    'type': 'answer_box'
                })
            
            return results
            
        except requests.exceptions.RequestException as e:
            return [{"error": f"Search request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Search error: {str(e)}"}]
    
    def search_news(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search for news articles using Serper API.
        
        Args:
            query (str): The search query
            num_results (int): Number of news results to return (default: 5)
            
        Returns:
            List[Dict]: List of news results
        """
        # Track news search attempt
        self.search_count += 1
        self.last_search_time = datetime.now()
        
        if not self.serper_api_key:
            return [{"error": "SERPER_API_KEY not found in environment variables"}]
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.post("https://google.serper.dev/news", headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'news' in data:
                news_count = len(data['news'][:num_results])
                for result in data['news'][:num_results]:
                    results.append({
                        'title': result.get('title', ''),
                        'link': result.get('link', ''),
                        'snippet': result.get('snippet', ''),
                        'date': result.get('date', ''),
                        'source': result.get('source', ''),
                        'type': 'news'
                    })
            
            return results
            
        except requests.exceptions.RequestException as e:
            return [{"error": f"News search request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"News search error: {str(e)}"}]
    
    def format_search_results(self, results: List[Dict]) -> str:
        """
        Format search results into a readable string for the AI agent.
        
        Args:
            results (List[Dict]): List of search results
            
        Returns:
            str: Formatted search results
        """
        if not results:
            return "No search results found."
        
        if len(results) == 1 and 'error' in results[0]:
            return f"Search error: {results[0]['error']}"
        
        formatted = "### Search Results:\n\n"
        
        for i, result in enumerate(results, 1):
            if 'error' in result:
                formatted += f"{i}. Error: {result['error']}\n\n"
                continue
                
            result_type = result.get('type', 'web')
            if result_type == 'answer_box':
                formatted += f"**Answer Box:**\n"
                formatted += f"- {result.get('snippet', '')}\n"
                if result.get('link'):
                    formatted += f"- Source: {result['link']}\n"
                formatted += "\n"
            elif result_type == 'news':
                formatted += f"{i}. **{result.get('title', 'No title')}**\n"
                formatted += f"   - Source: {result.get('source', 'Unknown')}\n"
                if result.get('date'):
                    formatted += f"   - Date: {result['date']}\n"
                formatted += f"   - Summary: {result.get('snippet', 'No summary available')}\n"
                formatted += f"   - Link: {result.get('link', '')}\n\n"
            else:
                formatted += f"{i}. **{result.get('title', 'No title')}**\n"
                formatted += f"   - Summary: {result.get('snippet', 'No summary available')}\n"
                if result.get('date'):
                    formatted += f"   - Date: {result['date']}\n"
                formatted += f"   - Link: {result.get('link', '')}\n\n"
        
        return formatted
    
    def get_search_stats(self) -> Dict:
        """
        Get statistics about web search usage.
        
        Returns:
            Dict: Search statistics including count and last search time
        """
        return {
            'total_searches': self.search_count,
            'last_search_time': self.last_search_time.isoformat() if self.last_search_time else None,
            'api_key_configured': bool(self.serper_api_key)
        }
    
    def print_search_stats(self):
        """Print search statistics to console."""
        stats = self.get_search_stats()
        print("\n" + "="*50)
        print("🔍 WEB SEARCH TOOL STATISTICS")
        print("="*50)
        print(f"Total Searches Performed: {stats['total_searches']}")
        print(f"API Key Configured: {'✅ Yes' if stats['api_key_configured'] else '❌ No'}")
        if stats['last_search_time']:
            print(f"Last Search Time: {stats['last_search_time']}")
        else:
            print("Last Search Time: Never")
        print("="*50)

# Global instance for easy access
web_search_tool = WebSearchTool()
