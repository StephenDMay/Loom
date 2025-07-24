#!/usr/bin/env python3
"""
Integration test for LLMManager functionality.
Tests core functionality without requiring external LLM libraries to be installed.
"""
import sys
import os
from unittest.mock import Mock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import ConfigManager
from agents.orchestrator import AgentOrchestrator
from agents.base_agent import BaseAgent

def test_basic_integration():
    """Test basic integration of LLMManager into the agent system."""
    print("Testing LLMManager integration...")
    
    # Create a mock config manager with minimal valid config
    config_manager = ConfigManager()
    config_manager._config = {
        "project": {
            "name": "Test",
            "context": "Test context",
            "tech_stack": "Python",
            "architecture": "Test arch",
            "target_users": "Developers",
            "constraints": "None"
        },
        "github": {
            "repo_owner": "test",
            "repo_name": "test",
            "default_project": "test",
            "default_labels": ["test"]
        },
        "llm_settings": {
            "default_provider": "gemini",
            "temperature": 0.7,
            "output_format": "structured",
            "research_depth": "standard"
        },
        "templates": {
            "directories": []
        },
        "automation": {
            "auto_create_issues": True,
            "auto_assign": True
        },
        "agent_execution_order": [],
        "agents": {
            "directory": "agents"
        }
    }
    
    try:
        # The orchestrator should now create successfully with lazy initialization
        orchestrator = AgentOrchestrator(config_manager)
        print("✅ AgentOrchestrator created successfully with LLMManager")
        
        # Verify LLMManager was created
        if hasattr(orchestrator, 'llm_manager') and orchestrator.llm_manager is not None:
            print("✅ LLMManager was created and attached to orchestrator")
            print(f"   Provider: {orchestrator.llm_manager.get_provider()}")
            return True
        else:
            print("❌ LLMManager was not created properly")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error during orchestrator creation: {e}")
        return False

def test_agent_inheritance():
    """Test that BaseAgent properly accepts LLMManager."""
    from core.llm_manager import LLMManager
    
    print("\nTesting BaseAgent LLMManager integration...")
    
    # Create a test agent
    class TestAgent(BaseAgent):
        def execute(self, *args, **kwargs):
            return f"Agent executed with LLM manager: {self.llm_manager is not None}"
    
    # Create mock LLM manager
    mock_llm_manager = Mock(spec=LLMManager)
    mock_llm_manager.get_provider.return_value = "gemini"
    
    # Test agent creation with LLM manager
    agent = TestAgent(config={}, llm_manager=mock_llm_manager)
    
    if agent.llm_manager is not None:
        print("✅ BaseAgent correctly accepts LLMManager instance")
        result = agent.execute()
        print(f"   Agent execution result: {result}")
        return True
    else:
        print("❌ BaseAgent did not properly store LLMManager")
        return False

def main():
    """Run all tests."""
    print("="*50)
    print("LLMManager Implementation Test")
    print("="*50)
    
    test1_passed = test_basic_integration()
    test2_passed = test_agent_inheritance()
    
    print("\n" + "="*50)
    print("Test Summary:")
    print(f"✅ Basic Integration: {'PASS' if test1_passed else 'FAIL'}")
    print(f"✅ Agent Inheritance: {'PASS' if test2_passed else 'FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All core functionality tests passed!")
        print("\nTo complete testing:")
        print("1. Set GEMINI_API_KEY environment variable")
        print("2. Install: pip install google-generativeai") 
        print("3. Run a real LLM call test")
        return True
    else:
        print("\n❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)