import unittest
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from agents.issue_generator.agent import IssueGeneratorAgent
from core.config_manager import ConfigManager

class TestIssueGeneratorAgent(unittest.TestCase):

    def setUp(self):
        # Mock ConfigManager to control configuration
        self.mock_config_manager = MagicMock(spec=ConfigManager)
        self.mock_config_manager.get.side_effect = self._mock_config_get

        # Create temporary directories for templates
        self.test_root_dir = Path("C:/Users/Steve/Projects/Loom/temp_test_root")
        self.test_root_dir.mkdir(parents=True, exist_ok=True)

        self.template_dir_1 = self.test_root_dir / "templates_1"
        self.template_dir_1.mkdir(exist_ok=True)
        (self.template_dir_1 / "meta-prompt-template.md").write_text("Template 1 content")

        self.template_dir_2 = self.test_root_dir / "templates_2"
        self.template_dir_2.mkdir(exist_ok=True)
        (self.template_dir_2 / "meta-prompt-template.md").write_text("Template 2 content")

        self.default_template_path = self.test_root_dir / "meta-prompt-template.md"
        self.default_template_path.write_text("Default template content")

        # Set up default mock config values
        self.mock_config_values = {
            "project.root": str(self.test_root_dir),
            "project.context": "Test Context",
            "project.tech_stack": "Test Tech Stack",
            "project.architecture": "Test Architecture",
            "project.target_users": "Test Users",
            "project.constraints": "Test Constraints",
            "llm_settings.default_provider": "mock_llm",
            "templates.directories": []
        }

    def tearDown(self):
        # Clean up temporary directories
        import shutil
        if self.test_root_dir.exists():
            shutil.rmtree(self.test_root_dir)

    def _mock_config_get(self, key, default=None):
        return self.mock_config_values.get(key, default)

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_find_template_path_success(self, mock_subprocess_run):
        self.mock_config_values["templates.directories"] = [str(self.template_dir_1.relative_to(self.test_root_dir))]
        agent = IssueGeneratorAgent(self.mock_config_manager)
        found_path = agent._find_template_path("meta-prompt-template.md")
        self.assertEqual(found_path, self.template_dir_1 / "meta-prompt-template.md")

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_find_template_path_multiple_directories(self, mock_subprocess_run):
        self.mock_config_values["templates.directories"] = [
            str(self.template_dir_1.relative_to(self.test_root_dir)),
            str(self.template_dir_2.relative_to(self.test_root_dir))
        ]
        agent = IssueGeneratorAgent(self.mock_config_manager)
        found_path = agent._find_template_path("meta-prompt-template.md")
        # Should find the first one
        self.assertEqual(found_path, self.template_dir_1 / "meta-prompt-template.md")

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_find_template_path_not_found(self, mock_subprocess_run):
        self.mock_config_values["templates.directories"] = [str(self.test_root_dir / "non_existent_dir")]
        agent = IssueGeneratorAgent(self.mock_config_manager)
        found_path = agent._find_template_path("non-existent-template.md")
        self.assertIsNone(found_path)

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_execute_with_configured_template(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = "Generated Issue Content"
        mock_subprocess_run.return_value.returncode = 0

        self.mock_config_values["templates.directories"] = [str(self.template_dir_1.relative_to(self.test_root_dir))]
        agent = IssueGeneratorAgent(self.mock_config_manager)
        
        result_path = agent.execute("Test feature description")
        
        self.assertTrue(Path(result_path).exists())
        with open(Path(result_path), 'r') as f:
            self.assertEqual(f.read(), "Generated Issue Content")
        
        # Verify that the correct template content was used in the prompt
        call_args = mock_subprocess_run.call_args[1]['input']
        self.assertIn("Template 1 content", call_args)

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_execute_with_default_template_fallback(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = "Generated Issue Content Default"
        mock_subprocess_run.return_value.returncode = 0

        # No templates.directories configured, or they don't contain the template
        self.mock_config_values["templates.directories"] = [str(self.test_root_dir / "another_non_existent_dir")]
        agent = IssueGeneratorAgent(self.mock_config_manager)
        
        result_path = agent.execute("Test feature description")
        
        self.assertTrue(Path(result_path).exists())
        with open(Path(result_path), 'r') as f:
            self.assertEqual(f.read(), "Generated Issue Content Default")
        
        # Verify that the default template content was used in the prompt
        call_args = mock_subprocess_run.call_args[1]['input']
        self.assertIn("Default template content", call_args)

    @patch('agents.issue_generator.agent.subprocess.run')
    def test_execute_template_not_found_error(self, mock_subprocess_run):
        # Ensure no template is found anywhere
        self.mock_config_values["templates.directories"] = [str(self.test_root_dir / "non_existent_dir")]
        
        # Remove the default template file so it can't be found either
        if self.default_template_path.exists():
            os.remove(self.default_template_path)

        agent = IssueGeneratorAgent(self.mock_config_manager)
        
        result = agent.execute("Test feature description")
        
        self.assertIn("Error: Meta-prompt template not found", result)
        self.assertFalse(mock_subprocess_run.called) # LLM should not be invoked

    def test_extract_title_from_markdown(self):
        agent = IssueGeneratorAgent(self.mock_config_manager)
        
        # Test with FEATURE: format
        content = "# FEATURE: Readable and Searchable Issue Filenames\n\n## EXECUTIVE SUMMARY"
        title = agent._extract_title_from_markdown(content)
        self.assertEqual(title, "Readable and Searchable Issue Filenames")
        
        # Test with regular heading
        content = "# Implement User Authentication\n\n## Details"
        title = agent._extract_title_from_markdown(content)
        self.assertEqual(title, "Implement User Authentication")
        
        # Test with no title
        content = "Some content without a proper title"
        title = agent._extract_title_from_markdown(content)
        self.assertEqual(title, "")

    def test_slugify(self):
        agent = IssueGeneratorAgent(self.mock_config_manager)
        
        # Test normal case
        slug = agent._slugify("Readable and Searchable Issue Filenames")
        self.assertEqual(slug, "readable-and-searchable-issue-filenames")
        
        # Test with special characters
        slug = agent._slugify("Feature: Add User @Auth & Permissions!")
        self.assertEqual(slug, "feature-add-user-auth-permissions")
        
        # Test with multiple spaces
        slug = agent._slugify("Multiple   Spaces    Here")
        self.assertEqual(slug, "multiple-spaces-here")
        
        # Test empty string
        slug = agent._slugify("")
        self.assertEqual(slug, "")
        
        # Test with leading/trailing spaces and hyphens
        slug = agent._slugify("  --Title with Issues--  ")
        self.assertEqual(slug, "title-with-issues")

if __name__ == '__main__':
    unittest.main()
