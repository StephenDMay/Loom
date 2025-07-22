#!/usr/bin/env python3
"""
Simple test script to verify the ProjectAnalysisAgent works correctly.
"""

import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from agents.project_analysis_agent.agent import ProjectAnalysisAgent
from core.config_manager import ConfigManager
from core.llm_manager import LLMManager
from core.context_manager import ContextManager


def test_project_analysis_agent():
    """Test the ProjectAnalysisAgent functionality."""
    print("Testing ProjectAnalysisAgent...")
    
    # Initialize managers
    config_manager = ConfigManager()
    context_manager = ContextManager()
    llm_manager = LLMManager(config_manager)
    
    # Create agent instance
    agent = ProjectAnalysisAgent(
        config={},
        llm_manager=llm_manager,
        context_manager=context_manager
    )
    
    # Execute the agent
    print("\nExecuting project analysis...")
    try:
        result = agent.execute()
        print(f"\nResult: {result}")
        
        # Check if context was stored
        
        stored_structure = context_manager.get("project_structure")
        if stored_structure:
            print(f"\n✅ Project structure successfully stored in context manager")
            print(f"Structure preview (first 500 chars):\n{stored_structure[:500]}...")
        else:
            print("\n❌ Project structure not found in context manager")
            
        stored_analysis = context_manager.get("project_analysis_summary")
        if stored_analysis:
            print(f"\n✅ Analysis summary successfully stored in context manager")
            print(f"Summary preview (first 300 chars):\n{stored_analysis[:300]}...")
        else:
            print("\n⚠️ Analysis summary not found in context manager (may be expected if LLM failed)")
        
        # Test template loading specifically
        test_template_loading(agent)
            
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


def test_template_loading(agent):
    """Test the template loading functionality specifically."""
    print("\n🧪 Testing template loading functionality...")
    
    from pathlib import Path
    
    # Test template loading with mock context
    template_path = Path(__file__).parent.parent.parent / "agents" / "project_analysis_agent" / "templates" / "project_analysis_template.md"
    
    test_context = {
        'project_name': 'TestProject',
        'tech_stack': 'Python',
        'architecture': 'Modular',
        'project_root': '/test/path',
        'feature_request': 'Add new feature',
        'directory_structure': 'test/\n  main.py',
        'key_files_content': 'No key files found'
    }
    
    try:
        processed_template = agent._load_and_prepare_template(template_path, test_context)
        
        # Verify that placeholders were replaced
        if '{{ project_name }}' not in processed_template and 'TestProject' in processed_template:
            print("✅ Template loading and placeholder replacement working correctly")
        else:
            print("❌ Template placeholders not properly replaced")
            
        # Check that template structure is maintained
        if "# Project Analysis Instructions" in processed_template:
            print("✅ Template structure preserved")
        else:
            print("❌ Template structure not preserved")
            
    except Exception as e:
        print(f"❌ Template loading test failed: {e}")
        
    # Test fallback behavior with non-existent template
    try:
        fake_path = Path("/nonexistent/template.md")
        agent._load_and_prepare_template(fake_path, test_context)
        print("❌ Template should have failed with non-existent file")
    except FileNotFoundError:
        print("✅ Proper error handling for missing template file")
    except Exception as e:
        print(f"❌ Unexpected error for missing template: {e}")


if __name__ == "__main__":
    success = test_project_analysis_agent()
    if success:
        print("\n🎉 ProjectAnalysisAgent test completed successfully!")
    else:
        print("\n💥 ProjectAnalysisAgent test failed!")
        sys.exit(1)