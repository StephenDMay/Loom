# FEATURE: Basic ConfigManager for JSON Loading

## EXECUTIVE SUMMARY
This feature introduces a `ConfigManager` class responsible for loading, parsing, and providing access to configuration from a JSON file. This centralizes configuration management, making the system more flexible and easier to maintain by removing hardcoded values.

## CODEBASE ANALYSIS
The project currently has a `dev-automation.config.json` file at the root, but no standardized way to access its contents. The main script, `dev-issue.py`, and the `AgentOrchestrator` in `agents/orchestrator.py` would benefit from a centralized configuration handler to manage settings like model choices, API keys (in a secure way), and agent-specific parameters. The `agents/example_agent/manifest.json` suggests that agents have their own configuration, which the `ConfigManager` could potentially be extended to handle in the future.

Integration points:
- `dev-issue.py`: Will be refactored to use the `ConfigManager` to load the main configuration file at startup.
- `agents/orchestrator.py`: Will use the `ConfigManager` to retrieve configuration needed for loading and running agents.

No significant architectural changes are required, but a new shared/core module will be created to house the `ConfigManager`.

## DOMAIN RESEARCH
In developer tools, configuration is critical for adapting the tool to different environments, projects, and user preferences. Common practice is to use a dedicated, easily-editable file format like JSON, YAML, or TOML. A singleton pattern for the configuration manager is a standard approach, ensuring that configuration is loaded once and is accessible globally, which prevents inconsistencies.

Key requirements for developers are:
- A predictable location for the configuration file.
- Clear error messages for missing or malformed files.
- An easy-to-use API for retrieving configuration values.

This feature aligns with the "Model API Differences" and "Cost Predictability" constraints by providing a foundation for managing different model settings and associated costs.

## TECHNICAL APPROACH
The recommended approach is to implement a `ConfigManager` class in Python using the standard `json` library. The class will be implemented as a singleton to ensure a single source of truth for configuration throughout the application's lifecycle.

The manager will be initialized at the start of the main script (`dev-issue.py`) with the path to `dev-automation.config.json`. It will parse the file and store the contents in a private dictionary. Public methods will provide read-only access to the configuration values.

**Alternative Approaches**:
1.  **Pydantic-based Config**: Use `pydantic` for data validation and type-hinted configuration models. This is a more robust solution but adds an external dependency and complexity not required for the initial "basic" implementation.
2.  **Environment Variables**: Exclusively use environment variables. This is good for security (especially for secrets) but less user-friendly for complex, nested configurations. A hybrid approach could be considered later.

The basic singleton class is chosen for its simplicity and lack of external dependencies, fitting the immediate need.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
No external API changes. The internal API of the `ConfigManager` will be:
```python
class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton implementation
        ...

    def load_config(self, config_path: str) -> None:
        # Loads and parses the JSON file
        ...

    def get(self, key: str, default: any = None) -> any:
        # Retrieves a value from the config
        ...
```

### Frontend Components
None. This is a backend/CLI feature.

### Backend Services
A new module will be created: `core/config_manager.py`.

**`ConfigManager` Class**:
- Implements the singleton pattern.
- `load_config(path)`: Takes a file path, reads the JSON, and stores it internally. It will raise `FileNotFoundError` if the path is invalid or a custom `ValueError` if the JSON is malformed.
- `get(key, default=None)`: Retrieves a configuration value. Can handle nested keys using dot notation (e.g., `"agent.settings.model"`).

## RISK ASSESSMENT
### Technical Risks
- **Risk 1**: Centralized config becomes a single point of failure.
  - **Mitigation**: Implement robust error handling for file I/O and parsing. Ensure fail-safes or sensible defaults where possible.
- **Risk 2**: Storing sensitive data (API keys) in plain text JSON is insecure.
  - **Mitigation**: For this initial implementation, we will proceed with the understanding that secrets should not be stored directly. A future enhancement will be required to integrate a secure secret management solution (e.g., environment variables, vault).

### Business Risks
- **Risk 1**: Poorly designed config structure could be confusing for developers.
  - **Mitigation**: Establish a clear, documented schema for `dev-automation.config.json` and provide examples.

## PROJECT DETAILS
**Estimated Effort**: 0.5 days
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to create**:
  - `core/__init__.py` (empty)
  - `core/config_manager.py`
  - `tests/core/test_config_manager.py`
- **Files to modify**:
  - `dev-issue.py`: To instantiate and use the `ConfigManager`.
  - `agents/orchestrator.py`: To use the `ConfigManager` instead of any hardcoded settings.
  - `.gitignore`: Add `tests/core/__pycache__/` and `core/__pycache__/`.
- **Key classes/functions to implement**:
  - `core.config_manager.ConfigManager`
- **CLI command structure**: No changes.
- **Acceptance criteria**: See below.

## SCOPE BOUNDARIES
**IN SCOPE**:
- A singleton `ConfigManager` class.
- Loading configuration from a single JSON file specified by a path.
- Accessing config values using a `get` method.
- Basic error handling for missing file and invalid JSON.
- Refactoring `dev-issue.py` to use the new manager.

**OUT OF SCOPE**:
- Support for other file formats (YAML, TOML, .env).
- Merging configurations from multiple sources.
- Environment variable overrides.
- Automatic configuration validation (e.g., using JSON Schema or Pydantic).
- Hot-reloading of configuration changes.
- Secure secret management.

## ACCEPTANCE CRITERIA
- [ ] A `ConfigManager` class exists in `core/config_manager.py`.
- [ ] The `ConfigManager` correctly loads a valid JSON file.
- [ ] The `ConfigManager.get()` method retrieves top-level and nested configuration values.
- [ ] The `ConfigManager` raises `FileNotFoundError` for a non-existent config file.
- [ ] The `ConfigManager` raises a `ValueError` for a malformed JSON file.
- [ ] The `ConfigManager` is implemented as a singleton, ensuring only one instance exists.
- [ ] `dev-issue.py` initializes and uses the `ConfigManager` to load `dev-automation.config.json`.
- [ ] Unit tests for the `ConfigManager` are implemented in `tests/core/test_config_manager.py`.

## GITHUB ISSUE TEMPLATE
**Title**: Feat: Create basic ConfigManager class with JSON config loading
**Labels**: feature, core, configuration
**Assignee**:
**Project**: Core System
