#!/usr/bin/env python3
"""
Web Search Tool Monitor - Track and analyze web search usage
"""

import json
from datetime import datetime
from pathlib import Path
from openai_agents.web_search import web_search_tool

class WebSearchMonitor:
    """Monitor and track web search tool usage."""
    
    def __init__(self, log_file: str = "web_search_usage.json"):
        self.log_file = Path(log_file)
        self.usage_data = self.load_usage_data()
    
    def load_usage_data(self) -> dict:
        """Load existing usage data from file."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {"sessions": [], "total_searches": 0}
    
    def save_usage_data(self):
        """Save usage data to file."""
        with open(self.log_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)
    
    def log_search_session(self, topic: str, search_count: int, include_news: bool = True):
        """Log a research session."""
        session = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "search_count": search_count,
            "include_news": include_news,
            "total_searches_before": self.usage_data["total_searches"]
        }
        
        self.usage_data["sessions"].append(session)
        self.usage_data["total_searches"] += search_count
        self.save_usage_data()
        
        print(f"📊 Logged research session: {search_count} searches for '{topic}'")
    
    def get_usage_summary(self) -> dict:
        """Get usage summary statistics."""
        sessions = self.usage_data["sessions"]
        
        if not sessions:
            return {
                "total_sessions": 0,
                "total_searches": 0,
                "avg_searches_per_session": 0,
                "most_recent_session": None,
                "most_researched_topics": []
            }
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_searches = self.usage_data["total_searches"]
        avg_searches = total_searches / total_sessions if total_sessions > 0 else 0
        
        # Find most researched topics
        topic_counts = {}
        for session in sessions:
            topic = session["topic"]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        most_researched = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_sessions": total_sessions,
            "total_searches": total_searches,
            "avg_searches_per_session": round(avg_searches, 2),
            "most_recent_session": sessions[-1] if sessions else None,
            "most_researched_topics": most_researched
        }
    
    def print_usage_report(self):
        """Print a detailed usage report."""
        summary = self.get_usage_summary()
        current_stats = web_search_tool.get_search_stats()
        
        print("\n" + "="*60)
        print("📊 WEB SEARCH TOOL USAGE REPORT")
        print("="*60)
        
        print(f"📈 Historical Data:")
        print(f"   Total Research Sessions: {summary['total_sessions']}")
        print(f"   Total Searches Performed: {summary['total_searches']}")
        print(f"   Average Searches per Session: {summary['avg_searches_per_session']}")
        
        if summary['most_recent_session']:
            recent = summary['most_recent_session']
            print(f"   Most Recent Session: {recent['topic']} ({recent['timestamp'][:19]})")
        
        print(f"\n🔍 Current Session:")
        print(f"   Searches in Current Session: {current_stats['total_searches']}")
        print(f"   API Key Status: {'✅ Configured' if current_stats['api_key_configured'] else '❌ Missing'}")
        
        if summary['most_researched_topics']:
            print(f"\n🏆 Most Researched Topics:")
            for i, (topic, count) in enumerate(summary['most_researched_topics'], 1):
                print(f"   {i}. {topic} ({count} session{'s' if count > 1 else ''})")
        
        print("="*60)
    
    def is_tool_being_used(self) -> bool:
        """Check if the web search tool is currently being used."""
        current_stats = web_search_tool.get_search_stats()
        return current_stats['total_searches'] > 0

# Global monitor instance
search_monitor = WebSearchMonitor()

def check_tool_usage():
    """Quick function to check if web search tool is being used."""
    if search_monitor.is_tool_being_used():
        print("✅ Web Search Tool IS being used!")
        web_search_tool.print_search_stats()
    else:
        print("❌ Web Search Tool is NOT being used yet.")
        print("   - Check if SERPER_API_KEY is set in your .env file")
        print("   - Try running a research query to see the tool in action")
    
    return search_monitor.is_tool_being_used()

if __name__ == "__main__":
    print("🔍 Web Search Tool Monitor")
    print("-" * 30)
    
    # Check current usage
    check_tool_usage()
    
    # Show full report
    search_monitor.print_usage_report()
