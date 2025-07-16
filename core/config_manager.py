import json
from typing import Any

class ConfigManager:
    _instance = None
    _config = {}

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
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in configuration file: {config_path} - {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the config.
        Can handle nested keys using dot notation (e.g., "agent.settings.model").
        """
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

config_manager = ConfigManager()
