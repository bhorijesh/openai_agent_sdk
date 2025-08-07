#!/usr/bin/env python3
"""
Simple example showing how to verify web search tool usage
"""

print("🔍 Web Search Tool Usage Verification")
print("="*50)

# Method 1: Check if API key is configured
print("\n1️⃣ Checking API Configuration...")
from openai_agents.web_search import web_search_tool

stats = web_search_tool.get_search_stats()
if stats['api_key_configured']:
    print("✅ SERPER_API_KEY is configured")
else:
    print("❌ SERPER_API_KEY is missing - add it to your .env file")

# Method 2: Test a simple search
print("\n2️⃣ Testing a simple search...")
try:
    results = web_search_tool.search("Python programming", num_results=2)
    if results and 'error' not in results[0]:
        print("✅ Web search is working!")
        print(f"   Found {len(results)} results")
    else:
        print("❌ Web search failed:")
        print(f"   Error: {results[0].get('error', 'Unknown error')}")
except Exception as e:
    print(f"❌ Exception during search: {e}")

# Method 3: Check usage statistics
print("\n3️⃣ Current usage statistics...")
web_search_tool.print_search_stats()

# Method 4: Test with researcher agent
print("\n4️⃣ Testing with Researcher Agent...")
try:
    from openai_agents.researcher import Researcher
    researcher = Researcher()
    
    print("🤖 Running quick research (watch for web search logs)...")
    result = researcher.quick_research("Machine Learning")
    
    if "[Error" not in result:
        print("✅ Researcher with web search is working!")
        print("   (Check the logs above for web search activity)")
    else:
        print("❌ Researcher failed:")
        print(f"   {result}")
        
except Exception as e:
    print(f"❌ Exception with researcher: {e}")

print("\n" + "="*50)
print("🎯 Summary: Look for the following signs that the tool is working:")
print("   🔍 Search log messages with queries and result counts")
print("   📊 Non-zero search statistics")
print("   ✅ Successful API responses")
print("   📄 Formatted search results in research output")
print("="*50)
