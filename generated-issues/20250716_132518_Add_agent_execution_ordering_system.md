# FEATURE: Add agent execution ordering system

## EXECUTIVE SUMMARY
This feature introduces a deterministic agent execution ordering system, allowing developers to define a specific sequence for agent workflows. By adding an `agent_execution_order` list to the global `dev-automation.config.json`, the `AgentOrchestrator` will execute agents in the specified order, enabling multi-step processes like 'research -> code -> test' and enhancing the system's automation capabilities.

## CODEBASE ANALYSIS
The current `AgentOrchestrator` in `agents/orchestrator.py` loads all agents from the `agents` directory into a dictionary, keyed by agent name. The order of loading is dependent on `os.listdir`, which is non-deterministic. The `dev-issue.py` script (specifically the `DevIssueRunner` class inside it, which seems to be the direction the CLI is heading) currently has a placeholder comment about needing a more sophisticated execution strategy.

The `ConfigManager` (`core/config_manager.py`) provides a centralized way to manage configuration and already supports loading a global `dev-automation.config.json`. This is the ideal place to define the execution order.

The integration point will be within the `AgentOrchestrator`. It will need to be modified to fetch the execution order from the `ConfigManager` after loading all agents and then sort them for execution.

## DOMAIN RESEARCH
In automated workflows and CI/CD pipelines, defining a clear, deterministic order of operations is standard practice. Systems like GitHub Actions use `needs` to define dependencies, while others like Prefect or Airflow use DAGs. For the current needs of this project, a simple, linear execution sequence is sufficient and avoids the complexity of a full dependency graph. This approach is easy for developers to understand and configure, directly addressing the pain point of running agents in a specific sequence for multi-stage tasks.

## TECHNICAL APPROACH
The recommended approach is to introduce a new optional key, `agent_execution_order`, in the main `dev-automation.config.json` file.

**Example `dev-automation.config.json`:**
```json
{
  "project": { ... },
  "llm_settings": { ... },
  "agent_execution_order": [
    "research_agent",
    "issue_generator",
    "coding_agent",
    "test_agent"
  ]
}
```

The `AgentOrchestrator` will:
1. Load all available agents from the filesystem into its `self.agents` dictionary as it does now.
2. Fetch the `agent_execution_order` list from `ConfigManager`.
3. Create a new ordered list of agent instances to be executed.
4. Iterate through the ordered list during execution.

**Handling Unordered Agents:**
- If an agent is present in the directory but not in the `agent_execution_order` list, it will not be executed. This makes the ordering list the single source of truth for which agents participate in a workflow.
- If the `agent_execution_order` key is missing from the config, the system will revert to the old behavior (executing all loaded agents in an arbitrary order) to maintain backward compatibility, but will print a warning.
- If the list contains an agent name that is not found, a clear error will be raised.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
No changes to external APIs. Internal method signatures in `AgentOrchestrator` will be updated.

### Frontend Components
None. This is a backend/CLI feature.

### Backend Services
**`core/config_manager.py`**: No changes required. The existing `get()` method is sufficient.

**`agents/orchestrator.py`**:
- Modify `__init__` or `load_agents` to build a sorted list of agents for execution.
- A new method `get_execution_sequence` will be added to return the ordered list of agents.
- The `execute_agent` method will be replaced by a method that runs the entire sequence, like `run_sequence`.

**`dev-issue.py`**:
- The main execution logic will call the new `run_sequence` method on the orchestrator, passing in the initial task.

## RISK ASSESSMENT
### Technical Risks
- **Risk 1**: Configuration errors (e.g., misspelled agent names in `agent_execution_order`).
  - **Mitigation**: The `AgentOrchestrator` will validate the `agent_execution_order` list against the list of loaded agents and raise a `ValueError` with a descriptive error message if an agent is not found.
- **Risk 2**: Breaking change for users who rely on the old "run all agents" behavior.
  - **Mitigation**: If `agent_execution_order` is not found in the config, the system will fall back to the previous behavior of using all discovered agents, printing a warning that recommends defining an explicit order.

### Business Risks
- **Risk 1**: Users may find it cumbersome to update the central config file.
  - **Mitigation**: This is a trade-off for explicit control. Documentation should be clear on how to configure the order. Future enhancements could include a CLI command to manage the sequence.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None. Relies on existing `ConfigManager` and `AgentOrchestrator` structure.
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to modify**:
  - `agents/orchestrator.py`: Implement the ordering logic.
  - `dev-issue.py`: Update the main runner to use the new execution sequence.
  - `dev-automation.config.json`: Add the `agent_execution_order` key with an example sequence.
  - `tests/core/test_orchestrator.py`: (New file or existing) Add unit tests for the ordering logic.

- **Key classes/functions to implement**:
  - `AgentOrchestrator.get_execution_sequence()`: Returns a list of agent instances sorted according to the config.
  - `AgentOrchestrator.run_sequence(initial_task)`: Iterates through the sorted agents, passing the output of one as the input to the next.
  - Update `AgentOrchestrator.__init__` to call the sorting logic.

- **CLI command structure**:
  No changes to the CLI command itself. The behavior of `python dev-issue.py "My task"` will be modified internally.

## SCOPE BOUNDARIES
**IN SCOPE**:
- A simple, linear execution order defined in `dev-automation.config.json`.
- The `AgentOrchestrator` respecting this order.
- Error handling for missing agents in the config list.
- Passing the output of agent `N` as the input to agent `N+1`.

**OUT OF SCOPE**:
- Complex dependency graphs (DAGs).
- Conditional execution (e.g., "run agent B only if agent A succeeds").
- Parallel execution of agents.
- Per-task execution ordering (the order is global for now).

## ACCEPTANCE CRITERIA
- [ ] When `agent_execution_order` is defined in `dev-automation.config.json`, agents are executed in that specific order.
- [ ] The output from a preceding agent is passed as the primary input to the subsequent agent.
- [ ] If an agent listed in the order is not found, the application exits with a clear error message.
- [ ] If `agent_execution_order` is not in the config, a warning is logged, and all found agents are executed in a non-guaranteed order.
- [ ] Agents not listed in `agent_execution_order` are not executed.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Implement Agent Execution Ordering System
**Labels**: enhancement, architecture, core
**Assignee**:
**Project**: Core Features
