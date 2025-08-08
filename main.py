#!/usr/bin/env python3
"""
Main entry point for the AI Blog Creation System.
This file handles user inputs and orchestrates the blog creation process.
"""

import sys
import os
from flow import agents
from datetime import datetime
from typing import Dict, Any

def get_default_blog_config() -> Dict[str, Any]:
    """Get default static blog configuration."""
    return {
        "word_count": 2000,
        "url": "",  
        "keywords": "remote work, benefits of remote work, work from home",  
        "tone": "professional",
        "language": "English",
        "audience": "general",
        "current_year": str(datetime.now().year),
        "faq": True,
        "topic": "The Benefits of Remote Work"
    }

def main():
    """Main function to handle the complete workflow."""
    try:
        # Create default configuration
        blog_config = get_default_blog_config()
        
        print(f"Starting blog creation with configuration:")
        
        result = agents.orchestrate_blog_creation(blog_config)
        
        print(f"\nBlog creation completed successfully!")
        print(f"Saved to: {result['saved_file']}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
