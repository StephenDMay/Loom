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
        self.malformed_config_path = os.path.join(self.test_dir, 'malformed_config.json')
        self.non_existent_config_path = os.path.join(self.test_dir, 'non_existent.json')

        self.config_data = {
            "key1": "value1",
            "nested": {
                "key2": "value2"
            },
            "agent": {
                "settings": {
                    "model": "gemini-pro"
                }
            }
        }

        with open(self.valid_config_path, 'w') as f:
            json.dump(self.config_data, f)

        with open(self.malformed_config_path, 'w') as f:
            f.write('{"key": "value",}')

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.valid_config_path):
            os.remove(self.valid_config_path)
        if os.path.exists(self.malformed_config_path):
            os.remove(self.malformed_config_path)
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
        self.assertEqual(self.config_manager._config, self.config_data)

    def test_load_config_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.config_manager.load_config(self.non_existent_config_path)

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

if __name__ == '__main__':
    unittest.main()
