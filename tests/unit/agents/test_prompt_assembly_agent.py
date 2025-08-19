#!/usr/bin/env python3

import unittest
import os
import tempfile
from unittest.mock import Mock
from pathlib import Path

# Add the project root to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from agents.prompt_assembly_agent.agent import PromptAssemblyAgent
from core.context_manager import ContextManager


class TestPromptAssemblyAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.context_manager = ContextManager()
        self.context_manager.set('project_name', 'Test Project')
        self.context_manager.set('user_name', 'Test User')
        
        self.agent = PromptAssemblyAgent(context_manager=self.context_manager)
        
        # Create a temporary template for testing
        self.test_template_content = """# {{ title }}

## Description
{{ description }}

## Context
Project: {{ context.project_name }}
User: {{ context.user_name }}

## Parameters
- Param1: {{ param1 }}
- Param2: {{ param2 }}"""
        
        # Create template file in the agent's templates directory
        self.agent.templates_path.mkdir(parents=True, exist_ok=True)
        self.test_template_path = self.agent.templates_path / 'test_template.md'
        with open(self.test_template_path, 'w') as f:
            f.write(self.test_template_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_template_path.exists():
            self.test_template_path.unlink()
    
    def test_load_template_success(self):
        """Test successful template loading."""
        content = self.agent._load_template('test_template')
        self.assertEqual(content, self.test_template_content)
    
    def test_load_template_with_extension(self):
        """Test template loading with .md extension."""
        content = self.agent._load_template('test_template.md')
        self.assertEqual(content, self.test_template_content)
    
    def test_load_template_not_found(self):
        """Test template loading with non-existent template."""
        with self.assertRaises(FileNotFoundError):
            self.agent._load_template('nonexistent_template')
    
    def test_get_context_values(self):
        """Test context value retrieval."""
        context_keys = ['project_name', 'user_name', 'nonexistent_key']
        context_values = self.agent._get_context_values(context_keys)
        
        expected = {
            'project_name': 'Test Project',
            'user_name': 'Test User',
            'nonexistent_key': ''  # Should handle missing keys gracefully
        }
        self.assertEqual(context_values, expected)
    
    def test_get_context_values_no_context_manager(self):
        """Test context value retrieval when no context manager is available."""
        agent_without_context = PromptAssemblyAgent()
        context_values = agent_without_context._get_context_values(['any_key'])
        self.assertEqual(context_values, {})
    
    def test_replace_placeholders(self):
        """Test placeholder replacement."""
        template = "Title: {{ title }}, Project: {{ context.project_name }}, Param: {{ param1 }}"
        placeholders = {'title': 'My Title', 'param1': 'Value1'}
        context_values = {'project_name': 'Test Project'}
        
        result = self.agent._replace_placeholders(template, placeholders, context_values)
        expected = "Title: My Title, Project: Test Project, Param: Value1"
        self.assertEqual(result, expected)
    
    def test_execute_success(self):
        """Test successful prompt assembly execution."""
        placeholders = {
            'title': 'Code Review',
            'description': 'Review the following code changes',
            'param1': 'Check security',
            'param2': 'Verify tests'
        }
        context_keys = ['project_name', 'user_name']
        
        result = self.agent.execute('test_template', placeholders, context_keys)
        
        # Verify the template was assembled correctly
        self.assertIn('# Code Review', result)
        self.assertIn('Review the following code changes', result)
        self.assertIn('Project: Test Project', result)
        self.assertIn('User: Test User', result)
        self.assertIn('Check security', result)
        self.assertIn('Verify tests', result)
        
        # Verify context was updated
        self.assertEqual(self.context_manager.get('assembled_prompt'), result)
        self.assertEqual(self.context_manager.get('last_template_used'), 'test_template')
    
    def test_execute_with_defaults(self):
        """Test execution with default parameters."""
        result = self.agent.execute('test_template')
        
        # Should work with empty placeholders and context
        self.assertIn('# {{ title }}', result)  # Unreplaced placeholder
        self.assertIn('Project: {{ context.project_name }}', result)  # Unreplaced context
    
    def test_execute_template_not_found(self):
        """Test execution with non-existent template."""
        with self.assertRaises(Exception) as context:
            self.agent.execute('nonexistent_template')
        
        self.assertIn('Prompt assembly failed', str(context.exception))
        
        # Verify error was stored in context
        error_msg = self.context_manager.get('prompt_assembly_error')
        self.assertIn('Prompt assembly failed', error_msg)
    
    def test_execute_no_context_manager(self):
        """Test execution without context manager."""
        agent_without_context = PromptAssemblyAgent()
        
        # Create template in the agent's templates directory
        agent_without_context.templates_path.mkdir(parents=True, exist_ok=True)
        test_template_path = agent_without_context.templates_path / 'simple_template.md'
        with open(test_template_path, 'w') as f:
            f.write('Simple template: {{ title }}')
        
        try:
            result = agent_without_context.execute('simple_template', {'title': 'Test'})
            self.assertEqual(result, 'Simple template: Test')
        finally:
            if test_template_path.exists():
                test_template_path.unlink()


if __name__ == '__main__':
    unittest.main()