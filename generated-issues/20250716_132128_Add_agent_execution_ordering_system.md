# FEATURE:"
    marker_pos = raw_result.find(feature_marker)
    if marker_pos > 0:
        result = raw_result[marker_pos:]

    with open(output_file, 'w') as f:
        f.write(result)
        
    # For agent-based execution, we return the path to the generated file
    return str(output_file)
Codebase analysis complete. Based on the review, here is the feature specification.

# FEATURE: Agent Execution Ordering System

## EXECUTIVE SUMMARY
This feature introduces a sequential agent execution pipeline, allowing the system to run a series of agents in a predefined order. This enables the creation of complex, multi-step automation workflows, where the output of one agent can be used as the input for the next, forming a chain of automated tasks.

## CODEBASE ANALYSIS
- **`AgentOrchestrator` (`agents/orchestrator.py`)**: Currently loads all agents and has a method `execute_agent` to run a single agent by name. It will be modified to handle a sequence of agents.
- **`BaseAgent` (`agents/base_agent.py`)**: The abstract `execute` method signature (`*args, **kwargs`) is flexible enough to handle passing state between agents without changes.
- **`ConfigManager` (`core/config_manager.py`)**: This singleton manages loading configuration from `dev-automation.config.json`. It will be used to retrieve the new agent sequence configuration.
- **`dev-issue.py`**: This CLI tool currently invokes a single process. It will be updated to trigger an agent sequence via the `AgentOrchestrator`.
- **`dev-automation.config.json`**: This file will be updated to include a new key, `agent_sequence`, which will define the order of agent execution.

## DOMAIN RESEARCH
- **User Workflows**: Developers need to chain operations, such as generating code, then generating tests for that code, and finally linting the result. A linear sequence is the most common and immediately useful pattern.
- **Industry Patterns**: Workflow systems like GitHub Actions use YAML files to define job sequences. AI frameworks like LangChain use "Chains" to link LLM calls. A simple list of agent names in a JSON config is a straightforward and effective starting point that aligns with these patterns.
- **State Management**: The core challenge is managing context between agents. A simple dictionary passed through the sequence is a common pattern. Each agent can read from and write to this dictionary, allowing for a shared state.

## TECHNICAL APPROACH
The recommended approach is to define a default agent sequence in the main `dev-automation.config.json` file. The `AgentOrchestrator` will be enhanced to read this sequence, execute the agents in order, and pass a shared context object between them.

1.  **Configuration**: Add an `agent_sequence` list to `dev-automation.config.json`.
2.  **Orchestrator Logic**: Create a new method `execute_sequence` in `AgentOrchestrator`. This method will:
    -   Initialize an empty context dictionary.
    -   Loop through the agent names in the sequence.
    -   Execute each agent, passing the context dictionary to its `execute` method.
    -   The agent's return value will update the context.
3.  **CLI Integration**: The `dev-issue.py` script will be modified to call `execute_sequence` on the orchestrator. The initial "task" or feature description will be the starting point for the context.

### Alternative Approaches
- **Separate Workflow Files**: Define workflows in separate files (e.g., `workflows.json`). This adds flexibility but also complexity. It is considered out of scope for this initial implementation.
- **Agent-Declared Dependencies**: Agents could declare their successor in their manifest. This creates tight coupling and is less flexible than a centralized definition.

## IMPLEMENTATION SPECIFICATION
### Database Changes
- No database changes are required.

### API Design
- No public-facing API changes are required. Internal method signatures will be updated.

### Frontend Components
- No frontend components are involved. This is a backend/CLI feature.

### Backend Services
- **`AgentOrchestrator`**:
    -   A new method `execute_sequence(sequence_name: str, initial_context: dict)` will be added.
    -   It will fetch the agent list from the config using `sequence_name`.
    -   It will manage a `context` dictionary, passing it to each agent and updating it with the agent's output.
- **`ConfigManager`**:
    -   No changes needed. The existing `get` method is sufficient.
- **`dev-automation.config.json`**:
    -   A new top-level key will be added:
        ```json
        "sequences": {
          "default_issue_generation": [
            "issue_generator",
            "file_writer_agent"
          ]
        }
        ```
- **`dev-issue.py`**:
    -   Will be refactored to use the `AgentOrchestrator` to run the `default_issue_generation` sequence.

## RISK ASSESSMENT
### Technical Risks
- **State Management**: The context object could become complex and hard to manage if not properly defined.
    - **Mitigation**: Start with a simple, well-documented dictionary structure for the context. For example: `{'task': '...', 'last_output': '...'}`.
- **Error Handling**: An agent failing mid-sequence could leave the system in an inconsistent state.
    - **Mitigation**: The orchestrator will stop execution immediately if any agent fails and will log a clear error message indicating which agent in the sequence failed.

### Business Risks
- **Limited Flexibility**: A simple linear sequence may not cover all user needs.
    - **Mitigation**: This initial implementation is a foundational step. More advanced features like conditional branching can be added later based on user feedback.

## PROJECT DETAILS
**Estimated Effort**: 2 days
**Dependencies**: None. Relies on existing project components.
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to Create/Modify**:
    -   `agents/orchestrator.py`: Modify to add `execute_sequence` logic.
    -   `dev-automation.config.json`: Add the `sequences` configuration.
    -   `dev-issue.py`: Refactor to use the orchestrator's new sequence execution.
- **Key Classes/Functions**:
    -   `AgentOrchestrator.execute_sequence()`
    -   The `main()` function in `dev-issue.py`.
- **CLI Command Structure**:
    -   The existing command `python dev-issue.py "feature description"` will now trigger the default sequence defined in the config.
- **Acceptance Criteria**:
    -   The system must execute agents in the order specified in `dev-automation.config.json`.
    -   The output from an agent must be available as input to the subsequent agent via a shared context.
    -   Execution must halt with a clear error if any agent in the sequence fails.

## SCOPE BOUNDARIES
- **IN SCOPE**:
    -   Executing a single, linear sequence of agents defined in the main config file.
    -   Passing a dictionary-based context object between agents.
    -   Updating the `dev-issue.py` CLI to use this new sequence-based execution model.
- **OUT OF SCOPE**:
    -   Conditional logic or branching within sequences.
    -   Parallel execution of agents.
    -   Defining multiple, named sequences that can be chosen at runtime via a CLI flag.
    -   A UI for managing sequences.

## ACCEPTANCE CRITERIA
- [ ] Configuration for an agent sequence can be defined in `dev-automation.config.json`.
- [ ] `AgentOrchestrator` can execute a named sequence of agents.
- [ ] A context dictionary is successfully passed from one agent to the next.
- [ ] The `dev-issue.py` command successfully triggers the default agent sequence.
- [ ] If an agent in the sequence raises an exception, the entire sequence stops execution.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Implement Agent Execution Ordering System
**Labels**: feature, architecture, orchestrator
**Assignee**:
**Project**: AutoDev-Board
