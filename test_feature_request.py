#!/usr/bin/env python3
"""
Quick test to verify feature request functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))

from agents.project_analysis_agent.agent import ProjectAnalysisAgent
from core.context_manager import ContextManager

def test_feature_request():
    """Quick test of feature request functionality."""
    print("Testing feature request functionality...")
    
    # Create agent with minimal setup
    context_manager = ContextManager()
    agent = ProjectAnalysisAgent(
        config={},
        llm_manager=None,  # Skip LLM for quick test
        context_manager=context_manager
    )
    
    # Test with feature request
    feature_request = "Add user authentication system"
    result = agent.execute(feature_request)
    
    print(f"✅ Agent executed with feature request: '{feature_request}'")
    print(f"Result contains authentication: {'authentication' in result.lower()}")
    
    # Check if project structure was stored
    structure = context_manager.get("project_structure")
    if structure:
        print("✅ Project structure stored in context")
    else:
        print("❌ Project structure not stored")
    
    return True

if __name__ == "__main__":
    test_feature_request()
    print("✅ Feature request test completed!")