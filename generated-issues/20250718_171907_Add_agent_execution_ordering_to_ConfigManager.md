# FEATURE: Add agent execution ordering to ConfigManager

## EXECUTIVE SUMMARY
This feature introduces a dedicated method within the `ConfigManager` to retrieve the agent execution order. This centralizes configuration-related logic, making the system more maintainable and aligning the `ConfigManager` with its responsibility as the single source of configuration truth.

## CODEBASE ANALYSIS
- **`core/config_manager.py`**: This is the main configuration handler. It currently has a generic `get(key)` method. A new, specific method `get_agent_execution_order()` will be added here to explicitly handle the agent execution sequence.
- **`agents/orchestrator.py`**: The `AgentOrchestrator` is currently responsible for fetching the agent execution order using `config_manager.get('agent_execution_order')`. This will be updated to call the new, more explicit `config_manager.get_agent_execution_order()` method. This change simplifies the orchestrator's logic and decouples it from the specific configuration key used to store the execution order.
- **`dev-automation.config.json`**: This file contains the `agent_execution_order` array, which defines the sequence of agents to be executed. No changes are required to this file, as the new `ConfigManager` method will read from this existing key.

## DOMAIN RESEARCH
In orchestration systems, it's a common pattern to have a centralized configuration manager that provides specific, well-defined accessors for different configuration properties. This avoids scattering knowledge of the configuration schema throughout the codebase. By creating a dedicated method for the agent execution order, we improve code clarity and make future changes to the configuration structure easier to manage. For example, if we later decide to support multiple execution chains, the logic for that can be encapsulated within the `ConfigManager` without requiring changes to the `AgentOrchestrator`.

## TECHNICAL APPROACH
The recommended approach is to add a new method `get_agent_execution_order()` to the `ConfigManager` class. This method will be responsible for retrieving the `agent_execution_order` list from the configuration. The `AgentOrchestrator` will then be updated to use this new method. This approach is straightforward, low-risk, and improves the overall architecture by better separating concerns.

An alternative approach would be to leave the logic in the `AgentOrchestrator`. However, this is not recommended as it violates the principle of centralized configuration management and makes the system harder to maintain in the long run.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required for this feature.

### API Design
No changes to external APIs are required. The change is internal to the application's architecture.

### Frontend Components
There is no frontend for this application, so no changes are required.

### Backend Services
- **`ConfigManager`**:
    - Add a new public method: `get_agent_execution_order() -> list[str]`
    - This method will access `self._config` to get the value of the `agent_execution_order` key.
- **`AgentOrchestrator`**:
    - In the `prepare_execution_sequence` method, replace the call to `self.config_manager.get('agent_execution_order')` with `self.config_manager.get_agent_execution_order()`.

## RISK ASSESSMENT
### Technical Risks
- **Minimal Risk**: The changes are localized to two files and are unlikely to have unintended side effects. The primary risk is a typo or logic error in the new method, which can be easily caught with unit tests.
    - **Mitigation**: Add a unit test for the new `get_agent_execution_order` method in `tests/core/test_config_manager.py`.

### Business Risks
- **No Business Risks**: This is a technical improvement and has no direct impact on users or business operations.

## PROJECT DETAILS
**Estimated Effort**: 1-2 hours
**Dependencies**: None
**Priority**: Medium
**Category**: Technical-debt

## IMPLEMENTATION DETAILS
- **Files to modify**:
    - `core/config_manager.py`
    - `agents/orchestrator.py`
    - `tests/core/test_config_manager.py` (to add a test)
- **Key classes/functions to implement**:
    - `ConfigManager.get_agent_execution_order()`
- **CLI command structure**: No changes to the CLI are required.
- **Acceptance criteria**:
    - The `AgentOrchestrator` successfully retrieves the agent execution order using the new `ConfigManager` method.
    - The application runs as expected with the changes.
    - A unit test for `get_agent_execution_order` is implemented and passes.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Creating the `get_agent_execution_order` method in `ConfigManager`.
- Updating `AgentOrchestrator` to use the new method.
- Adding a unit test for the new method.

**OUT OF SCOPE**:
- Supporting multiple execution chains.
- Changing the format of the `agent_execution_order` in the configuration file.
- Adding any new configuration options.

## ACCEPTANCE CRITERIA
- [ ] A new method `get_agent_execution_order` exists in the `ConfigManager` class.
- [ ] The `AgentOrchestrator` class calls the new `get_agent_execution_order` method.
- [ ] The application correctly executes the agents in the order specified in `dev-automation.config.json`.
- [ ] A unit test for `get_agent_execution_order` is added and passes.

## GITHUB ISSUE TEMPLATE
**Title**: Refactor: Add get_agent_execution_order method to ConfigManager
**Labels**: `refactor`, `technical-debt`, `config`
**Assignee**:
**Project**: AutoDev-Board
