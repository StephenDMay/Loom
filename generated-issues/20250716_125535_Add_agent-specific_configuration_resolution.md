# FEATURE: Agent-Specific Configuration Resolution

## EXECUTIVE SUMMARY
This feature introduces a hierarchical configuration system, allowing individual agents to have their own `config.json` file. This file will supplement or override the global configuration, providing granular control over agent-specific settings like models, API keys, or prompts.

## CODEBASE ANALYSIS
- **`core/config_manager.py`**: Currently a singleton that loads a single, global configuration file. It will be modified to support loading a base configuration and merging a secondary, agent-specific configuration file on top of it.
- **`agents/orchestrator.py`**: This class is responsible for loading agents. It will be updated to detect the presence of an `agent.json` file within an agent's directory and use the `ConfigManager` to create a merged configuration to pass to the agent instance.
- **`agents/base_agent.py`**: The `BaseAgent` constructor already accepts a `config` dictionary. No changes are required here, as it's already prepared to accept the resolved configuration from the orchestrator.
- **Integration Points**: The primary integration point is between the `AgentOrchestrator` and the `ConfigManager`. The orchestrator will trigger the new merging logic in the `ConfigManager` during the agent loading process.

## DOMAIN RESEARCH
- **User Workflows**: Developers often need to experiment with a single agent's settings (e.g., changing the temperature for a creative writing agent vs. a code generation agent) without altering the global configuration. This feature enables that workflow by isolating configuration to the agent's directory.
- **Industry Patterns**: Hierarchical configuration is a standard pattern. A common approach is: `global config` <- `user config` <- `project config` <- `instance config`. This feature implements a two-level hierarchy: `global config` <- `agent config`. This is a robust and well-understood model.
- **Competitive Analysis**: Many plugin and extension-based systems (like VS Code extensions or Jenkins plugins) allow for per-plugin configuration, which validates the need for this pattern.

## TECHNICAL APPROACH
The recommended approach is to enhance `ConfigManager` to handle layered configurations.

1.  Create a new method in `ConfigManager`, `get_agent_config(agent_name, agent_config_path)`, or similar.
2.  This method will first load the global configuration as a base.
3.  It will then load the agent-specific JSON file from `agent_config_path`.
4.  A deep merge will be performed, where keys from the agent's config will recursively update/overwrite keys from the global config.
5.  The `AgentOrchestrator` will, for each agent, check for a `config.json`. If it exists, it will call the new `ConfigManager` method and pass the resulting merged dictionary to the agent's constructor.

An alternative would be to have the `AgentOrchestrator` perform the merge itself. This is less desirable as it violates separation of concerns; configuration management should remain centralized in the `ConfigManager`.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
No external API changes. The internal API of `ConfigManager` will be modified.

**`ConfigManager` New Method:**
```python
def get_merged_config(self, base_config_path: str, override_config_path: str) -> dict:
    """Loads a base config and deeply merges an override config on top of it."""
    # ... implementation ...
```

### Frontend Components
None.

### Backend Services
**`core/config_manager.py`**:
- Add a new method to perform a deep merge of two dictionaries.
- Modify `load_config` to optionally take a path, or add a new method like `load_and_merge(global_path, agent_path)` that returns a *new* config dictionary rather than modifying the singleton's state, to ensure different agents get their distinct configs.

**`agents/orchestrator.py`**:
- In `load_agents`, after identifying an agent's directory, check for the existence of `config.json`.
- If `config.json` exists, call the `ConfigManager` to get the merged configuration.
- If it does not exist, use the global configuration as is.
- Pass the final, resolved configuration to the agent's constructor: `agent_class(config=resolved_config)`.

## RISK ASSESSMENT
### Technical Risks
- **Complex Merge Logic**: A naive `dict.update()` is insufficient for nested structures. A recursive deep merge function must be implemented correctly. **Mitigation**: Implement a well-defined deep merge utility and add specific unit tests for nested key overrides, list handling, and type mismatches.
- **Configuration State Bleeding**: If the singleton `ConfigManager`'s state is modified directly by each agent's config, agents loaded later will incorrectly inherit settings from previously loaded agents. **Mitigation**: The `ConfigManager` should not modify its global `_config` state. Instead, it should return a *new, merged dictionary* for each agent that has a custom configuration.

### Business Risks
- **User Confusion**: If the configuration resolution order is not clearly documented, users may be confused about why certain settings are or are not being applied. **Mitigation**: Clearly document the `global -> agent` override behavior in the project's `README.md` or other relevant documentation.

## PROJECT DETAILS
**Estimated Effort**: 1-2 days
**Dependencies**: None. This is a foundational change.
**Priority**: High
**Category**: Feature

## IMPLEMENTATION DETAILS
- **Files to Create**:
  - `tests/core/test_config_manager.py` (if not already robust enough)
  - `agents/issue_generator/config.json` (for testing purposes)
- **Files to Modify**:
  - `core/config_manager.py`
  - `agents/orchestrator.py`
- **Key Classes/Functions to Implement**:
  - `ConfigManager._deep_merge(base: dict, override: dict) -> dict`
  - `ConfigManager.get_agent_config(agent_name: str) -> dict` (or similar logic)
  - Modify `AgentOrchestrator.load_agents()` to incorporate the new logic.
- **CLI Command Structure**: No changes to the CLI are required. This is a backend architectural change.

## SCOPE BOUNDARIES
**IN SCOPE**:
- An agent can have a `config.json` in its root directory.
- This configuration will be deeply merged on top of the global configuration.
- The merged configuration is passed to the agent upon initialization.

**OUT OF SCOPE**:
- Dynamic, real-time reloading of configuration changes.
- Environment variable-based configuration overrides for this feature.
- More than two levels of configuration hierarchy (e.g., user-level configs).

## ACCEPTANCE CRITERIA
- [ ] A `_deep_merge` utility is added to `ConfigManager` and is covered by unit tests.
- [ ] `AgentOrchestrator` looks for `config.json` in each agent's directory.
- [ ] If `config.json` is found, `AgentOrchestrator` requests a merged configuration from `ConfigManager`.
- [ ] An agent without a `config.json` receives the standard global configuration.
- [ ] An agent *with* a `config.json` receives a correctly merged configuration, with its local values overriding global ones.
- [ ] An integration test confirms that an agent's behavior changes based on the values in its `config.json`.

## GITHUB ISSUE TEMPLATE
**Title**: Feat: Implement Agent-Specific Configuration Resolution
**Labels**: enhancement, architecture, configuration
**Assignee**:
**Project**: Core System
