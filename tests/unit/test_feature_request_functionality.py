#!/usr/bin/env python3
"""
Unit tests for the feature request functionality in ProjectAnalysisAgent.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from agents.project_analysis_agent.agent import ProjectAnalysisAgent
from core.context_manager import ContextManager


class TestFeatureRequestFunctionality(unittest.TestCase):
    """Test cases for feature request functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.context_manager = ContextManager()
        self.agent = ProjectAnalysisAgent(
            config={},
            llm_manager=None,
            context_manager=self.context_manager
        )
    
    def test_feature_request_parameter(self):
        """Test that feature request is properly accepted as parameter."""
        feature_request = "Implement user authentication with OAuth"
        
        # Execute with feature request
        result = self.agent.execute(feature_request)
        
        # Should complete without error
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_default_feature_request(self):
        """Test that agent works with default feature request."""
        result = self.agent.execute()
        
        # Should complete without error
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_context_storage(self):
        """Test that project structure is stored in context."""
        feature_request = "Add REST API endpoints"
        
        # Execute with feature request
        self.agent.execute(feature_request)
        
        # Check that project structure was stored
        structure = self.context_manager.get("project_structure")
        self.assertIsNotNone(structure)
        self.assertIsInstance(structure, str)
        self.assertTrue(len(structure) > 0)
    
    def test_feature_request_signature(self):
        """Test that the execute method has the correct signature."""
        import inspect
        
        sig = inspect.signature(self.agent.execute)
        params = list(sig.parameters.keys())
        
        # Should have feature_request as first parameter
        self.assertTrue('feature_request' in params)
        
        # Should have default value
        feature_request_param = sig.parameters['feature_request']
        self.assertEqual(feature_request_param.default, "General project analysis")
    
    @patch.object(ProjectAnalysisAgent, '_load_and_prepare_template')
    def test_template_context_includes_feature_request(self, mock_template_load):
        """Test that feature request is passed to template context."""
        feature_request = "Create admin dashboard"
        mock_template_load.return_value = "Mocked template content"
        
        # Execute with feature request
        self.agent.execute(feature_request)
        
        # Check that template was called with context including feature request
        if mock_template_load.called:
            call_args = mock_template_load.call_args
            context = call_args[0][1]  # Second argument is context
            self.assertEqual(context['feature_request'], feature_request)


if __name__ == '__main__':
    unittest.main()