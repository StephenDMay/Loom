import json
from typing import Any, Dict
import copy

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def load_config(self, config_path: str) -> None:
        """
        Loads and parses the JSON file.
        Raises FileNotFoundError if the path is invalid or ValueError if the JSON is malformed.
        """
        try:
            with open(config_path, 'r') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            # It's okay for the global config to not exist, just means we have an empty config
            self._config = {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in configuration file: {config_path} - {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the config.
        Can handle nested keys using dot notation (e.g., "agent.settings.model").
        """
        return self._get_from_dict(self._config, key, default)

    def get_config(self) -> Dict[str, Any]:
        """Returns a copy of the entire configuration dictionary."""
        return copy.deepcopy(self._config)

    def get_merged_config(self, override_config_path: str) -> Dict[str, Any]:
        """
        Loads an override config and deeply merges it on top of the base config.
        Returns a new dictionary and does not modify the singleton's state.
        """
        base_config = self.get_config()
        try:
            with open(override_config_path, 'r') as f:
                override_config = json.load(f)
        except FileNotFoundError:
            # If the agent-specific config doesn't exist, return the base config
            return base_config
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in override configuration file: {override_config_path} - {e}")

        return self._deep_merge(base_config, override_config)

    @staticmethod
    def _deep_merge(base: Dict, override: Dict) -> Dict:
        """
        Recursively merges two dictionaries.
        `override` values take precedence over `base` values.
        """
        merged = copy.deepcopy(base)
        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = ConfigManager._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _get_from_dict(self, config_dict: Dict, key: str, default: Any = None) -> Any:
        """
        Helper to retrieve a value from a specific dictionary.
        """
        keys = key.split('.')
        value = config_dict
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

config_manager = ConfigManager()
