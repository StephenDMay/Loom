# FEATURE: Add get_agent_config method to ConfigManager

## EXECUTIVE SUMMARY
This feature introduces a new method to the `ConfigManager` class, `get_agent_config`, which retrieves the configuration for a specific agent by merging the agent's `config.json` with the base configuration. This simplifies agent-specific configuration management and ensures that agents have access to the correct settings.

## CODEBASE ANALYSIS
The `ConfigManager` class in `core/config_manager.py` is a singleton responsible for managing the application's configuration. It currently has a `get_merged_config` method that can merge a base configuration with an override file. The `AgentOrchestrator` in `agents/orchestrator.py` is responsible for loading and managing agents. It currently passes the global `ConfigManager` instance to each agent.

The proposed `get_agent_config` method will leverage the existing `get_merged_config` method to provide a clear and concise way to retrieve agent-specific configurations. This will involve locating the agent's `config.json` file and using it as the override configuration.

## DOMAIN RESEARCH
In a multi-agent system, it's common for individual agents to have their own specific configurations that override global settings. This allows for greater flexibility and modularity, as agents can be configured independently without affecting the entire system. The proposed feature aligns with this pattern by providing a dedicated method for retrieving agent-specific configurations.

## TECHNICAL APPROACH
The recommended approach is to add a `get_agent_config(self, agent_name: str)` method to the `ConfigManager` class. This method will:

1.  Construct the path to the agent's `config.json` file based on the agent's name and the configured agents directory.
2.  Call the existing `get_merged_config` method with the path to the agent's `config.json` file.
3.  Return the merged configuration.

This approach is simple, efficient, and reuses existing code.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required.

### API Design
No API changes are required.

### Frontend Components
No frontend components are affected.

### Backend Services
- **`core/config_manager.py`**:
    - Add a new method `get_agent_config(self, agent_name: str) -> Dict[str, Any]`.
- **`agents/orchestrator.py`**:
    - Modify the `load_agents` method to use `config_manager.get_agent_config(agent_name)` when initializing each agent.

## RISK ASSESSMENT
### Technical Risks
- **Incorrect path resolution**: The method needs to correctly resolve the path to the agent's configuration file. This can be mitigated by using the `agents.directory` configuration setting and robust path manipulation.
- **Configuration conflicts**: If there are conflicting keys between the base and agent configurations, the agent's configuration should take precedence. The existing `_deep_merge` method already handles this correctly.

### Business Risks
- **Misconfiguration**: If an agent's configuration is not set up correctly, it may not function as expected. This can be mitigated by providing clear documentation and examples.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to modify**:
    - `core/config_manager.py`
    - `agents/orchestrator.py`
    - `tests/core/test_config_manager.py`
- **Key classes/functions to implement**:
    - `ConfigManager.get_agent_config(self, agent_name: str)`
- **CLI command structure**: No changes to the CLI are required.
- **Acceptance criteria**:
    - The `get_agent_config` method should return a dictionary containing the merged configuration.
    - The agent's configuration should override the base configuration.
    - If an agent does not have a `config.json` file, the method should return the base configuration.
    - The `AgentOrchestrator` should use the new method to load agent configurations.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Adding the `get_agent_config` method to `ConfigManager`.
- Updating `AgentOrchestrator` to use the new method.
- Adding unit tests for the new method.

**OUT OF SCOPE**:
- Modifying the structure of agent configuration files.
- Adding new configuration settings for agents.

## ACCEPTANCE CRITERIA
- [ ] The `get_agent_config` method is implemented in `core/config_manager.py`.
- [ ] The `AgentOrchestrator` is updated to use `get_agent_config`.
- [ ] Unit tests for `get_agent_config` are added to `tests/core/test_config_manager.py`.
- [ ] All existing tests pass.

## GITHUB ISSUE TEMPLATE
**Title**: Add get_agent_config method to ConfigManager
**Labels**: feature, enhancement
**Assignee**:
**Project**: AutoDev-Board
