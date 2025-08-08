import sys
import os
from flow import agents
from datetime import datetime
from typing import Dict, Any
import time

def get_default_blog_config() -> Dict[str, Any]:
    """Get default static blog configuration."""
    return {
        "word_count": 2000,
        "url": "",  
        "keywords": "nike shoes, running shoes, athletic footwear",  
        "tone": "professional",
        "language": "English",
        "audience": "general",
        "current_year": str(datetime.now().year),
        "faq":False,
        "topic": ""
    }

def main():
    """Main function to handle the complete workflow."""
    # Create default configuration
    start =time.time()
    blog_config = get_default_blog_config()
    print(f"Starting blog creation with configuration:")
    result = agents.orchestrate_blog_creation(blog_config)
    print(f"\nBlog creation completed successfully!")
    end = time.time()
    print(f"Total time taken: {(end - start)/60:.2f} minutes")

    
if __name__ == "__main__":
    main()
