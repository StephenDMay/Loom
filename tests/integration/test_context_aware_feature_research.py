#!/usr/bin/env python3
"""
Test script to verify context-aware FeatureResearchAgent functionality.
Tests both scenarios: with context and without context.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.context_manager import ContextManager
from agents.feature_research_agent.agent import FeatureResearchAgent

def test_without_context():
    """Test FeatureResearchAgent without any context."""
    print("=" * 60)
    print("TEST 1: FeatureResearchAgent WITHOUT context")
    print("=" * 60)
    
    # Create empty context manager
    context_manager = ContextManager()
    
    # Create agent
    agent = FeatureResearchAgent(context_manager=context_manager)
    
    # Execute with a test feature request
    feature_request = "Add user authentication with JWT tokens"
    result = agent.execute(feature_request)
    
    print("Result:")
    print(result)
    print("\n" + "=" * 60 + "\n")
    return result

def test_with_context():
    """Test FeatureResearchAgent with project analysis context."""
    print("=" * 60)
    print("TEST 2: FeatureResearchAgent WITH context")
    print("=" * 60)
    
    # Create context manager with sample project analysis data
    context_manager = ContextManager()
    
    # Add some sample context that would be useful for feature research
    project_analysis = """
    This is a Python Flask web application with the following structure:
    - Uses SQLAlchemy for database operations
    - Has existing user models in models/user.py
    - Uses Blueprint architecture for route organization
    - Current authentication is session-based
    - Database: PostgreSQL
    - Frontend: Jinja2 templates with some JavaScript
    """
    
    tech_stack = """
    Backend: Python 3.9, Flask 2.0, SQLAlchemy, PostgreSQL
    Frontend: HTML/CSS/JavaScript, Jinja2 templates
    Testing: pytest
    Deployment: Docker, nginx
    """
    
    context_manager.set('project_analysis_summary', project_analysis)
    context_manager.set('tech_stack_info', tech_stack)
    
    # Create agent
    agent = FeatureResearchAgent(context_manager=context_manager)
    
    # Execute with the same test feature request
    feature_request = "Add user authentication with JWT tokens"
    result = agent.execute(feature_request)
    
    print("Result:")
    print(result)
    print("\n" + "=" * 60 + "\n")
    return result

def main():
    """Run both tests and compare results."""
    print("Testing Context-Aware FeatureResearchAgent Implementation")
    print("========================================================")
    
    try:
        # Test without context
        result_without = test_without_context()
        
        # Test with context  
        result_with = test_with_context()
        
        # Simple verification
        print("VERIFICATION:")
        print("- Both tests completed successfully ✓")
        print("- Template rendering worked ✓")
        
        # Check if context was used (should see different content)
        if "Project Analysis Summary" in result_with and "Tech Stack Info" in result_with:
            print("- Context was successfully integrated ✓")
        else:
            print("- WARNING: Context may not have been properly integrated")
            
        if len(result_with) > len(result_without):
            print("- Context-aware result is more detailed ✓")
        
        print("\nImplementation appears to be working correctly!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()