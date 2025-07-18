import json
from typing import Any, Dict
import copy
from pathlib import Path

from jsonschema import validate, ValidationError

class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}
    _schema: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_schema()
            cls._config = {} # Initialize _config for the new instance
        return cls._instance

    def _load_schema(self) -> None:
        schema_path = Path(__file__).parent / "config_schema.json"
        try:
            with open(schema_path, 'r') as f:
                self._schema = json.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"Configuration schema file not found: {schema_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in configuration schema file: {schema_path} - {e}")

    def load_config(self, config_path: str) -> None:
        """
        Loads and parses the JSON file and validates it against the schema.
        Raises FileNotFoundError if the path is invalid or ValueError if the JSON is malformed.
        Raises ConfigValidationError if the config does not match the schema.
        """
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
            self._validate_config(loaded_config)
            self._config = loaded_config
        except FileNotFoundError:
            # It's okay for the global config to not exist, just means we have an empty config
            self._config = {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in configuration file: {config_path} - {e}")

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validates the given configuration dictionary against the loaded schema.
        Raises ConfigValidationError if validation fails.
        """
        try:
            validate(instance=config, schema=self._schema)
        except ValidationError as e:
            raise ConfigValidationError(f"Configuration validation error: {e.message} in {e.path}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the config.
        Can handle nested keys using dot notation (e.g., "agent.settings.model").
        """
        return self._get_from_dict(self._config, key, default)

    def get_config(self) -> Dict[str, Any]:
        """
        Returns a copy of the entire configuration dictionary.
        """
        return copy.deepcopy(self._config)

    def get_merged_config(self, override_config_path: str) -> Dict[str, Any]:
        """
        Loads an override config and deeply merges it on top of the base config.
        Validates the merged configuration.
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

        merged_config = self._deep_merge(base_config, override_config)
        self._validate_config(merged_config) # Validate the merged config
        return merged_config

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Retrieves the configuration for a specific agent by merging the agent's
        config.json with the base configuration.
        Returns the merged configuration dictionary.
        """
        agents_directory = self.get("agents.directory", "agents")
        agent_config_path = Path(agents_directory) / agent_name / "config.json"
        return self.get_merged_config(str(agent_config_path))

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

    def get_agent_execution_order(self) -> list[str]:
        """
        Retrieves the agent execution order from the configuration.
        Returns the list of agent names in execution order.
        """
        return self.get('agent_execution_order', [])

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value in the config.
        Can handle nested keys using dot notation (e.g., "agent.settings.model").
        """
        keys = key.split('.')
        d = self._config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

class AgentConfigManager:
    """
    A wrapper around ConfigManager that provides agent-specific configuration access.
    """
    def __init__(self, base_config_manager: ConfigManager, agent_name: str):
        self._base_config_manager = base_config_manager
        self._agent_name = agent_name
        self._agent_config = None
        
    def _get_agent_config(self):
        """Lazy-load the agent-specific configuration."""
        if self._agent_config is None:
            self._agent_config = self._base_config_manager.get_agent_config(self._agent_name)
        return self._agent_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the agent-specific merged config.
        Can handle nested keys using dot notation.
        """
        agent_config = self._get_agent_config()
        return self._base_config_manager._get_from_dict(agent_config, key, default)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Returns a copy of the agent-specific merged configuration.
        """
        return copy.deepcopy(self._get_agent_config())
    
    def set(self, key: str, value: Any) -> None:
        """
        Delegates to the base config manager for global settings.
        """
        return self._base_config_manager.set(key, value)

config_manager = ConfigManager()
