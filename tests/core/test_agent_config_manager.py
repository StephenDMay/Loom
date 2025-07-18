import unittest
import json
import os
from pathlib import Path
from core.config_manager import ConfigManager, AgentConfigManager

class TestAgentConfigManager(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance before each test
        ConfigManager._instance = None
        self.config_manager = ConfigManager()
        
        self.test_dir = Path('tests/core/temp_test_agent_configs')
        os.makedirs(self.test_dir, exist_ok=True)

        # Set up agent test directories and configs
        self.agents_dir = self.test_dir / 'agents'
        self.test_agent_dir = self.agents_dir / 'test_agent'
        os.makedirs(self.test_agent_dir, exist_ok=True)
        self.agent_config_path = self.test_agent_dir / 'config.json'

        self.base_config_data = {
            "project": {
                "name": "TestProject",
                "context": "A test project context.",
                "tech_stack": "Python",
                "architecture": "Modular",
                "target_users": "Developers",
                "constraints": "None"
            },
            "github": {
                "repo_owner": "test_owner",
                "repo_name": "test_repo",
                "default_project": "TestBoard",
                "default_labels": ["bug", "feature"]
            },
            "llm_settings": {
                "default_provider": "gemini",
                "output_format": "structured",
                "research_depth": "standard",
                "temperature": 0.7
            },
            "templates": {
                "directories": ["templates"]
            },
            "automation": {
                "auto_create_issues": True,
                "auto_assign": False
            },
            "agent_execution_order": ["agent1", "agent2"],
            "agents": {
                "directory": str(self.agents_dir)
            }
        }
        
        self.agent_config_data = {
            "llm_settings": {
                "default_provider": "claude",
                "temperature": 0.5
            },
            "agent_specific_setting": "test_value"
        }

        self.base_config_path = self.test_dir / 'base_config.json'
        with open(self.base_config_path, 'w') as f:
            json.dump(self.base_config_data, f)
            
        with open(self.agent_config_path, 'w') as f:
            json.dump(self.agent_config_data, f)

    def tearDown(self):
        # Clean up created files and directories
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        # Reset singleton after tests
        ConfigManager._instance = None

    def test_agent_config_manager_merges_config(self):
        self.config_manager.load_config(str(self.base_config_path))
        agent_config_manager = AgentConfigManager(self.config_manager, 'test_agent')
        
        # Agent config should override base config values
        self.assertEqual(agent_config_manager.get('llm_settings.default_provider'), 'claude')
        self.assertEqual(agent_config_manager.get('llm_settings.temperature'), 0.5)
        self.assertEqual(agent_config_manager.get('agent_specific_setting'), 'test_value')
        
        # Base config values should still be present where not overridden
        self.assertEqual(agent_config_manager.get('project.name'), 'TestProject')
        self.assertEqual(agent_config_manager.get('llm_settings.output_format'), 'structured')

    def test_agent_config_manager_no_agent_config(self):
        self.config_manager.load_config(str(self.base_config_path))
        agent_config_manager = AgentConfigManager(self.config_manager, 'nonexistent_agent')
        
        # Should return the base config values
        self.assertEqual(agent_config_manager.get('llm_settings.default_provider'), 'gemini')
        self.assertEqual(agent_config_manager.get('project.name'), 'TestProject')

    def test_agent_config_manager_get_config(self):
        self.config_manager.load_config(str(self.base_config_path))
        agent_config_manager = AgentConfigManager(self.config_manager, 'test_agent')
        
        full_config = agent_config_manager.get_config()
        
        # Should be a merged configuration
        self.assertEqual(full_config['llm_settings']['default_provider'], 'claude')
        self.assertEqual(full_config['project']['name'], 'TestProject')
        self.assertEqual(full_config['agent_specific_setting'], 'test_value')

    def test_agent_config_manager_lazy_loading(self):
        self.config_manager.load_config(str(self.base_config_path))
        agent_config_manager = AgentConfigManager(self.config_manager, 'test_agent')
        
        # Config should not be loaded yet
        self.assertIsNone(agent_config_manager._agent_config)
        
        # First access should load the config
        agent_config_manager.get('project.name')
        self.assertIsNotNone(agent_config_manager._agent_config)

if __name__ == '__main__':
    unittest.main()