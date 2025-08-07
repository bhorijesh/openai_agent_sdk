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

def get_user_input():
    """Get blog topic from user with validation."""
    while True:
        topic = input("Enter the blog topic (or 'quit' to exit): ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            return None
            
        if not topic:
            continue
            
        if len(topic) < 3:
            continue
            
        return topic

def display_progress_header(topic):
    """Display a nice header for the blog creation process."""
    pass

def display_completion_message(result, csv_filename):
    """Display completion message with preview."""
    pass

def ask_continue():
    """Ask user if they want to create another blog post."""
    while True:
        choice = input("\nWould you like to create another blog post? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            continue

def main():
    """Main function to handle the complete workflow."""
    try:
        while True:
            # Get user input
            topic = get_user_input()
            if topic is None:  # User chose to quit
                break
                
            try:
                display_progress_header(topic)
                
                # Create the blog
                result = agents.orchestrate_blog_creation(topic)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).rstrip()
                safe_topic = safe_topic.replace(' ', '_')[:30]
                csv_filename = f"blog_{safe_topic}_{timestamp}.csv"
                
                # Display completion message
                display_completion_message(result, csv_filename)
                
                # Ask if user wants to continue
                if not ask_continue():
                    break
                    
            except KeyboardInterrupt:
                if not ask_continue():
                    break
                    
            except Exception as e:
                if not ask_continue():
                    break
                    
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
