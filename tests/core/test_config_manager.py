import unittest
import json
import os
from pathlib import Path
from core.config_manager import ConfigManager, ConfigValidationError

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance before each test
        ConfigManager._instance = None
        # Initialize ConfigManager to load schema
        self.config_manager = ConfigManager()
        
        self.test_dir = Path('tests/core/temp_test_configs')
        os.makedirs(self.test_dir, exist_ok=True)

        self.valid_config_path = self.test_dir / 'valid_config.json'
        self.override_config_path = self.test_dir / 'override_config.json'
        self.malformed_config_path = self.test_dir / 'malformed_config.json'
        self.non_existent_config_path = self.test_dir / 'non_existent.json'
        self.invalid_config_path = self.test_dir / 'invalid_config.json'
        self.invalid_override_path = self.test_dir / 'invalid_override.json'
        
        # Set up agent test directories and configs
        self.agents_dir = self.test_dir / 'agents'
        self.test_agent_dir = self.agents_dir / 'test_agent'
        os.makedirs(self.test_agent_dir, exist_ok=True)
        self.agent_config_path = self.test_agent_dir / 'config.json'


        self.base_valid_config_data = {
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
        
        self.override_config_data = {
            "llm_settings": {
                "default_provider": "openai",
                "temperature": 0.9
            },
            "templates": {
                "directories": ["custom_templates"]
            }
        }

        with open(self.valid_config_path, 'w') as f:
            json.dump(self.base_valid_config_data, f)
            
        with open(self.override_config_path, 'w') as f:
            json.dump(self.override_config_data, f)

        with open(self.malformed_config_path, 'w') as f:
            f.write('{"key": "value",}')
        
        # Create an invalid config file for testing validation errors
        import copy
        invalid_data = copy.deepcopy(self.base_valid_config_data)
        invalid_data['llm_settings']['default_provider'] = 'unsupported_llm' # Invalid enum value
        with open(self.invalid_config_path, 'w') as f:
            json.dump(invalid_data, f)

        # Create an invalid override config that would make the merged config invalid
        invalid_override_data = {
            "llm_settings": {
                "default_provider": 123 # Wrong type
            }
        }
        with open(self.invalid_override_path, 'w') as f:
            json.dump(invalid_override_data, f)
            
        # Create agent config for testing
        self.agent_config_data = {
            "llm_settings": {
                "default_provider": "claude",
                "temperature": 0.5
            },
            "agent_specific_setting": "test_value"
        }
        with open(self.agent_config_path, 'w') as f:
            json.dump(self.agent_config_data, f)


    def tearDown(self):
        # Clean up created files and directories
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        # Reset singleton after tests
        ConfigManager._instance = None


    def test_singleton_instance(self):
        instance1 = ConfigManager()
        instance2 = ConfigManager()
        self.assertIs(instance1, instance2)

    def test_load_config_success(self):
        self.config_manager.load_config(str(self.valid_config_path))
        self.assertEqual(self.config_manager.get_config(), self.base_valid_config_data)

    def test_load_config_file_not_found(self):
        # Should not raise an error, just result in an empty config
        self.config_manager.load_config(str(self.non_existent_config_path))
        self.assertEqual(self.config_manager.get_config(), {})

    def test_load_config_malformed_json(self):
        with self.assertRaises(ValueError):
            self.config_manager.load_config(str(self.malformed_config_path))

    def test_load_config_invalid_schema_missing_field(self):
        # Create a config missing a required field
        invalid_data = self.base_valid_config_data.copy()
        del invalid_data['project']['name']
        with open(self.invalid_config_path, 'w') as f:
            json.dump(invalid_data, f)
        
        with self.assertRaises(ConfigValidationError) as cm:
            self.config_manager.load_config(str(self.invalid_config_path))
        self.assertIn("'name' is a required property", str(cm.exception))

    def test_load_config_invalid_schema_wrong_type(self):
        # Create a config with wrong type
        invalid_data = self.base_valid_config_data.copy()
        invalid_data['llm_settings']['temperature'] = "high" # Should be number
        with open(self.invalid_config_path, 'w') as f:
            json.dump(invalid_data, f)
        
        with self.assertRaises(ConfigValidationError) as cm:
            self.config_manager.load_config(str(self.invalid_config_path))
        self.assertIn("'high' is not of type 'number'", str(cm.exception))

    def test_load_config_invalid_schema_enum_value(self):
        # Use the pre-created invalid_config_path with unsupported_llm
        with self.assertRaises(ConfigValidationError) as cm:
            self.config_manager.load_config(str(self.invalid_config_path))
        self.assertIn("'unsupported_llm' is not one of ['gemini', 'openai', 'claude']", str(cm.exception))

    def test_get_top_level_key(self):
        self.config_manager.load_config(str(self.valid_config_path))
        self.assertEqual(self.config_manager.get("project.name"), "TestProject")

    def test_get_nested_key(self):
        self.config_manager.load_config(str(self.valid_config_path))
        self.assertEqual(self.config_manager.get("llm_settings.default_provider"), "gemini")
        self.assertEqual(self.config_manager.get("github.default_labels")[0], "bug")

    def test_get_non_existent_key(self):
        self.config_manager.load_config(str(self.valid_config_path))
        self.assertIsNone(self.config_manager.get("non.existent.key"))

    def test_get_key_with_default_value(self):
        self.config_manager.load_config(str(self.valid_config_path))
        default_value = "default"
        self.assertEqual(self.config_manager.get("non.existent.key", default=default_value), default_value)

    def test_deep_merge(self):
        merged = ConfigManager._deep_merge(self.base_valid_config_data, self.override_config_data)
        
        # Test overrides
        self.assertEqual(merged['llm_settings']['default_provider'], 'openai')
        self.assertEqual(merged['llm_settings']['temperature'], 0.9)
        self.assertEqual(merged['templates']['directories'], ['custom_templates'])
        
        # Test preservation of base keys
        self.assertEqual(merged['project']['name'], 'TestProject')
        self.assertEqual(merged['github']['repo_owner'], 'test_owner')
        self.assertEqual(merged['automation']['auto_create_issues'], True)

    def test_get_merged_config_success(self):
        self.config_manager.load_config(str(self.valid_config_path))
        merged_config = self.config_manager.get_merged_config(str(self.override_config_path))
        
        import copy
        expected_merged = copy.deepcopy(self.base_valid_config_data)
        expected_merged['llm_settings']['default_provider'] = 'openai'
        expected_merged['llm_settings']['temperature'] = 0.9
        expected_merged['templates']['directories'] = ['custom_templates']

        self.assertEqual(merged_config, expected_merged)
        
        # Verify the original config is not modified
        original_config = self.config_manager.get_config()
        self.assertEqual(original_config['llm_settings']['default_provider'], 'gemini')  # Should still be original value

    def test_get_merged_config_with_non_existent_override(self):
        self.config_manager.load_config(str(self.valid_config_path))
        merged_config = self.config_manager.get_merged_config(str(self.non_existent_config_path))
        self.assertEqual(merged_config, self.base_valid_config_data)

    def test_get_merged_config_invalid_merged_result(self):
        self.config_manager.load_config(str(self.valid_config_path))
        # The invalid_override_path will make llm_settings.default_provider an int, which is invalid
        with self.assertRaises(ConfigValidationError) as cm:
            self.config_manager.get_merged_config(str(self.invalid_override_path))
        self.assertIn("123 is not of type 'string'", str(cm.exception))
        self.assertIn("123 is not of type 'string'", str(cm.exception))

    def test_get_agent_config_success(self):
        self.config_manager.load_config(str(self.valid_config_path))
        agent_config = self.config_manager.get_agent_config('test_agent')
        
        # Agent config should override base config values
        self.assertEqual(agent_config['llm_settings']['default_provider'], 'claude')
        self.assertEqual(agent_config['llm_settings']['temperature'], 0.5)
        self.assertEqual(agent_config['agent_specific_setting'], 'test_value')
        
        # Base config values should still be present where not overridden
        self.assertEqual(agent_config['project']['name'], 'TestProject')
        self.assertEqual(agent_config['llm_settings']['output_format'], 'structured')

    def test_get_agent_config_no_agent_config_file(self):
        self.config_manager.load_config(str(self.valid_config_path))
        # Test with an agent that doesn't have a config.json file
        agent_config = self.config_manager.get_agent_config('nonexistent_agent')
        
        # Should return the base config unchanged
        expected_config = self.config_manager.get_config()
        self.assertEqual(agent_config, expected_config)

    def test_get_agent_config_uses_configured_agents_directory(self):
        self.config_manager.load_config(str(self.valid_config_path))
        agent_config = self.config_manager.get_agent_config('test_agent')
        
        # Should successfully find the agent config using the configured agents directory
        self.assertEqual(agent_config['agent_specific_setting'], 'test_value')

    def test_get_agent_config_defaults_to_agents_directory(self):
        # Test with a config that doesn't specify agents.directory
        import copy
        config_without_agents_dir = copy.deepcopy(self.base_valid_config_data)
        del config_without_agents_dir['agents']
        
        config_path_no_agents_dir = self.test_dir / 'config_no_agents_dir.json'
        with open(config_path_no_agents_dir, 'w') as f:
            json.dump(config_without_agents_dir, f)
        
        # Reset the singleton and create a new instance
        ConfigManager._instance = None
        test_config_manager = ConfigManager()
        test_config_manager.load_config(str(config_path_no_agents_dir))
        
        # Should default to "agents" directory
        agent_config = test_config_manager.get_agent_config('test_agent')
        # This should return base config since the agent won't be found in default "agents" dir
        expected_config = test_config_manager.get_config()
        self.assertEqual(agent_config, expected_config)


if __name__ == '__main__':
    unittest.main()
