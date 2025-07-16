import unittest
import json
import os
from core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance before each test
        ConfigManager._instance = None
        self.config_manager = ConfigManager()
        
        self.test_dir = 'tests/core/temp_test_configs'
        os.makedirs(self.test_dir, exist_ok=True)

        self.valid_config_path = os.path.join(self.test_dir, 'valid_config.json')
        self.override_config_path = os.path.join(self.test_dir, 'override_config.json')
        self.malformed_config_path = os.path.join(self.test_dir, 'malformed_config.json')
        self.non_existent_config_path = os.path.join(self.test_dir, 'non_existent.json')

        self.config_data = {
            "key1": "value1",
            "nested": {
                "key2": "value2",
                "key3": "value3"
            },
            "agent": {
                "settings": {
                    "model": "gemini-pro",
                    "temperature": 0.5
                }
            }
        }
        
        self.override_config_data = {
            "key1": "override_value1",
            "nested": {
                "key2": "override_value2"
            },
            "agent": {
                "settings": {
                    "model": "gemini-ultra"
                }
            },
            "new_key": "new_value"
        }

        with open(self.valid_config_path, 'w') as f:
            json.dump(self.config_data, f)
            
        with open(self.override_config_path, 'w') as f:
            json.dump(self.override_config_data, f)

        with open(self.malformed_config_path, 'w') as f:
            f.write('{"key": "value",}')

    def tearDown(self):
        # Clean up created files
        for path in [self.valid_config_path, self.override_config_path, self.malformed_config_path]:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        # Reset singleton after tests
        ConfigManager._instance = None


    def test_singleton_instance(self):
        instance1 = ConfigManager()
        instance2 = ConfigManager()
        self.assertIs(instance1, instance2)

    def test_load_config_success(self):
        self.config_manager.load_config(self.valid_config_path)
        self.assertEqual(self.config_manager.get_config(), self.config_data)

    def test_load_config_file_not_found(self):
        # Should not raise an error, just result in an empty config
        self.config_manager.load_config(self.non_existent_config_path)
        self.assertEqual(self.config_manager.get_config(), {})

    def test_load_config_malformed_json(self):
        with self.assertRaises(ValueError):
            self.config_manager.load_config(self.malformed_config_path)

    def test_get_top_level_key(self):
        self.config_manager.load_config(self.valid_config_path)
        self.assertEqual(self.config_manager.get("key1"), "value1")

    def test_get_nested_key(self):
        self.config_manager.load_config(self.valid_config_path)
        self.assertEqual(self.config_manager.get("nested.key2"), "value2")
        self.assertEqual(self.config_manager.get("agent.settings.model"), "gemini-pro")

    def test_get_non_existent_key(self):
        self.config_manager.load_config(self.valid_config_path)
        self.assertIsNone(self.config_manager.get("non.existent.key"))

    def test_get_key_with_default_value(self):
        self.config_manager.load_config(self.valid_config_path)
        default_value = "default"
        self.assertEqual(self.config_manager.get("non.existent.key", default=default_value), default_value)

    def test_deep_merge(self):
        merged = ConfigManager._deep_merge(self.config_data, self.override_config_data)
        
        # Test overrides
        self.assertEqual(merged['key1'], 'override_value1')
        self.assertEqual(merged['nested']['key2'], 'override_value2')
        self.assertEqual(merged['agent']['settings']['model'], 'gemini-ultra')
        
        # Test preservation of base keys
        self.assertEqual(merged['nested']['key3'], 'value3')
        self.assertEqual(merged['agent']['settings']['temperature'], 0.5)
        
        # Test addition of new keys
        self.assertEqual(merged['new_key'], 'new_value')

    def test_get_merged_config(self):
        self.config_manager.load_config(self.valid_config_path)
        merged_config = self.config_manager.get_merged_config(self.override_config_path)
        
        # Verify the merged result
        self.assertEqual(merged_config['key1'], 'override_value1')
        self.assertEqual(merged_config['nested']['key2'], 'override_value2')
        self.assertEqual(merged_config['nested']['key3'], 'value3')
        self.assertEqual(merged_config['agent']['settings']['model'], 'gemini-ultra')
        self.assertEqual(merged_config['agent']['settings']['temperature'], 0.5)
        self.assertEqual(merged_config['new_key'], 'new_value')
        
        # Verify the original config is not modified
        self.assertEqual(self.config_manager.get_config(), self.config_data)

    def test_get_merged_config_with_non_existent_override(self):
        self.config_manager.load_config(self.valid_config_path)
        merged_config = self.config_manager.get_merged_config(self.non_existent_config_path)
        self.assertEqual(merged_config, self.config_data)


if __name__ == '__main__':
    unittest.main()
