#!/usr/bin/env python3
"""
Test script for the enhanced Researcher agent with web search capabilities.
Demonstrates logging and monitoring features.
"""

from openai_agents.researcher import Researcher
import logging

# Set up console logging to see web search activities
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def test_researcher():
    """Test the researcher agent with web search functionality."""
    print("🔍 Testing Enhanced Researcher Agent with Web Search\n")
    print("📊 Watch the console for real-time logging of web search activities!\n")
    
    # Initialize the researcher
    researcher = Researcher()
    
    # Show initial search statistics
    researcher.web_search.print_search_stats()
    
    # Test topic
    topic = "Artificial Intelligence in Healthcare 2025"
    
    print(f"\n🎯 Research Topic: {topic}\n")
    print("=" * 60)
    
    # Test quick research without news
    print("⚡ Quick Research (no news):")
    print("-" * 40)
    quick_result = researcher.quick_research(topic)
    print(quick_result)
    
    print("\n" + "=" * 60)
    
    # Test full research with news
    print("📰 Full Research (including news):")
    print("-" * 40)
    result = researcher.run(topic, include_news=True)
    print(result)
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed! Check the logs above to see web search tool usage.")

def test_web_search_directly():
    """Test the web search tool directly to see it in action."""
    from tools.web_search import web_search_tool
    
    print("\n🔧 Testing Web Search Tool Directly")
    print("=" * 50)
    
    # Test a simple search
    results = web_search_tool.search("Python programming tutorials", num_results=3)
    formatted = web_search_tool.format_search_results(results)
    print(formatted)
    
    # Show search statistics
    web_search_tool.print_search_stats()

if __name__ == "__main__":
    print("Choose a test:")
    print("1. Test Researcher Agent (recommended)")
    print("2. Test Web Search Tool directly")
    print("3. Both")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_researcher()
    elif choice == "2":
        test_web_search_directly()
    elif choice == "3":
        test_web_search_directly()
        print("\n" + "="*80 + "\n")
        test_researcher()
    else:
        print("Invalid choice. Running researcher test...")
        test_researcher()
