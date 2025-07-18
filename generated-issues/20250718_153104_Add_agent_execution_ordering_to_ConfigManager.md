# FEATURE: Add agent execution ordering to ConfigManager

## EXECUTIVE SUMMARY
This feature centralizes the logic for retrieving the agent execution order into the `ConfigManager`. This improves separation of concerns by making `ConfigManager` the sole authority on configuration access and decouples the `AgentOrchestrator` from the specific structure of the configuration file.

## CODEBASE ANALYSIS
- **`core/config_manager.py`**: This is the primary file to be modified. It currently provides generic configuration access via a `get()` method. A new, specific method `get_agent_execution_order()` will be added to encapsulate the logic for retrieving the execution sequence.
- **`agents/orchestrator.py`**: This component currently fetches the execution order using `config_manager.get('agent_execution_order')`. It will be refactored to use the new, more explicit method from the `ConfigManager`.
- **`dev-automation.config.json`**: The configuration file already contains the `agent_execution_order` key. No changes are required to the file itself.
- **`core/config_schema.json`**: The schema already validates that `agent_execution_order` is an array of strings. No changes are needed.

## DOMAIN RESEARCH
- **User Workflows**: A developer defines a sequence of agent executions in a configuration file to create a processing pipeline. The system must reliably execute agents in this specified order. The current implementation supports this but can be made more robust and maintainable.
- **Industry Patterns**: It is a standard best practice to encapsulate and centralize configuration logic. A dedicated configuration management component should provide a clear, high-level interface for other services, hiding implementation details like configuration file keys and default values. This is an application of the Facade design pattern.
- **Competitive Solutions**: Systems with plugin or agent architectures (e.g., CI/CD pipelines, data processing frameworks) universally rely on a core component to parse and provide execution ordering, rather than having each component query raw configuration data.

## TECHNICAL APPROACH
The recommended implementation is to add a new method, `get_agent_execution_order()`, to the `ConfigManager` class. This method will be responsible for retrieving the `agent_execution_order` list from the configuration, using the existing `get()` method internally and providing an empty list `[]` as a default if the key is not specified. Subsequently, the `AgentOrchestrator` will be refactored to use this new method, simplifying its implementation and decoupling it from the configuration key.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
No changes to external or service-level APIs. The following public method will be added to the `ConfigManager` Python class:
- `ConfigManager.get_agent_execution_order() -> list[str]`

### Frontend Components
None.

### Backend Services
- **`ConfigManager`**: Will be modified to include the new `get_agent_execution_order` method.
- **`AgentOrchestrator`**: Its `prepare_execution_sequence` method will be updated to call the new `ConfigManager` method.

## RISK ASSESSMENT
### Technical Risks
- **[Risk 1]**: Minimal risk of regression. The change is a simple refactoring that moves logic without altering it.
- **[Mitigation]**: The change is small and self-contained. Existing tests for the `AgentOrchestrator` should continue to pass, and a new unit test for the `ConfigManager` method can be added to ensure correctness.

### Business Risks  
- **[Risk 1]**: None. This is a non-functional, technical improvement with no impact on user-facing features.

## PROJECT DETAILS
**Estimated Effort**: < 1 day
**Dependencies**: None
**Priority**: Medium
**Category**: technical-debt

## IMPLEMENTATION DETAILS
- **Specific files to create/modify**:
    1. `/home/steve/storage/projects/Loom/core/config_manager.py` (Modify)
    2. `/home/steve/storage/projects/Loom/agents/orchestrator.py` (Modify)

- **Key classes/functions to implement**:
    - In `core/config_manager.py`, add the following method to the `ConfigManager` class:
      ```python
      def get_agent_execution_order(self) -> list[str]:
          """
          Retrieves the agent execution order from the configuration.
          Returns an empty list if not specified.
          """
          return self.get('agent_execution_order', [])
      ```

- **Key classes/functions to modify**:
    - In `agents/orchestrator.py`, modify the `prepare_execution_sequence` method:
        - **From**: `agent_order_names = self.config_manager.get('agent_execution_order')`
        - **To**: `agent_order_names = self.config_manager.get_agent_execution_order()`

- **Exact CLI command structure**: No changes to the CLI.

## SCOPE BOUNDARIES
**What is explicitly IN scope for this feature?**
- Creating the `get_agent_execution_order` method in `ConfigManager`.
- Refactoring `AgentOrchestrator` to use the new method.

**What is explicitly OUT of scope and should be separate features?**
- Changing the data structure of the execution order in the JSON config.
- Adding validation logic to `ConfigManager` to check if agents in the list exist (This responsibility correctly remains with the `AgentOrchestrator`).

## ACCEPTANCE CRITERIA
- [ ] A method `get_agent_execution_order()` is implemented on `ConfigManager`.
- [ ] The new method returns the `agent_execution_order` list from the config, or an empty list if it's not present.
- [ ] `AgentOrchestrator.prepare_execution_sequence()` is updated to use `get_agent_execution_order()`.
- [ ] The application's agent execution behavior is unchanged.

## GITHUB ISSUE TEMPLATE
**Title**: Refactor: Centralize Agent Execution Order Logic in ConfigManager
**Labels**: enhancement, refactor, config
**Assignee**: 
**Project**: Loom
