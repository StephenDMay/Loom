# FEATURE: Modular Agent System with Dedicated Prompt Templates

## EXECUTIVE SUMMARY
This feature introduces a modular agent system to replace the monolithic script (`dev-issue.py`). This will allow for specialized, reusable agents (e.g., "CodeGenerator", "CodeReviewer") each with its own dedicated prompt template, improving maintainability, scalability, and output consistency across different AI models.

## CODEBASE ANALYSIS
The current system is centered around `dev-issue.py`, a single script that handles configuration, prompt assembly, and LLM interaction. The `templates/` directory contains simple wrapper scripts (`api.py`, `ui.py`, etc.) that pass a template type to the main script, indicating a desire for specialization. The `ProjectVision.md` and `LongTermGoal.md` documents explicitly call for a more modular, multi-stage, and model-agnostic architecture, which this feature directly addresses.

This change will deprecate the monolithic approach in `dev-issue.py` in favor of a new `agents` directory and a central `AgentOrchestrator`. It's a significant architectural refactoring but aligns perfectly with the stated project vision.

## DOMAIN RESEARCH
Modern AI development frameworks (LangChain, CrewAI, Autogen) have proven the value of modular, agent-based architectures. Developers using these systems can compose complex workflows from smaller, single-purpose agents. The primary pain point this solves is the difficulty of managing massive, all-purpose prompts that are hard to debug and lead to inconsistent outputs.

By giving each agent a dedicated, version-controlled prompt template, we can:
1.  **Standardize Inputs/Outputs**: Ensure each agent performs its task predictably.
2.  **Improve Reusability**: Use a "DocstringAgent" in multiple workflows.
3.  **Simplify Maintenance**: Update an agent's prompt without affecting the entire system.
4.  **Facilitate Model-Specific Optimization**: Tailor an agent's prompt template to the strengths of a specific AI model (e.g., one for code generation, another for review).

## TECHNICAL APPROACH
The recommended approach is to create a new `agents` directory and an `AgentOrchestrator` class to manage them.

1.  **Agent Structure**: Create an `agents/` directory at the project root. Each agent will be a subdirectory (e.g., `agents/code_generator/`).
    -   `agents/code_generator/agent.py`: Contains the agent's logic (a class inheriting from a `BaseAgent`).
    -   `agents/code_generator/prompt.md`: The Jinja2-enabled markdown prompt template for this agent.
    -   `agents/code_generator/config.json`: (Optional) Agent-specific configuration.

2.  **Base Classes**:
    -   `BaseAgent`: An abstract class defining the agent interface (e.g., `execute(self, context)`).
    -   `AgentOrchestrator`: A class responsible for discovering, loading, and running agents. It will replace the core logic of `dev-issue.py`.

3.  **Prompt Templating**: Use Jinja2 for powerful prompt templating, allowing loops, conditionals, and variable substitution within the `.md` files.

4.  **Refactor `dev-issue.py`**: The existing script will be refactored to become a simple CLI entry point that uses the `AgentOrchestrator` to execute the requested agent and task.

An alternative is to use a plugin-based system like `pluggy`, but a simple directory-based discovery mechanism is sufficient for the initial implementation and avoids adding a new dependency.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required.

### API Design
The primary change is to the internal Python API.

-   **New Directory**: `agents/`
-   **New/Modified Classes**:
    -   `src/agents/base.py`:
        -   `class BaseAgent(ABC)`: Defines `__init__(self, config)` and `@abstractmethod execute(self, context: dict) -> str`.
    -   `src/orchestration/orchestrator.py`:
        -   `class AgentOrchestrator`:
            -   `discover_agents(self, path)`: Scans the `agents` directory.
            -   `get_agent(self, agent_name)`: Loads and initializes a specific agent.
            -   `run(self, agent_name, context)`: Executes an agent with given context.
    -   `dev-issue.py`: Refactor `main()` and `generate_issue()` to use `AgentOrchestrator`. The CLI arguments will change to `python dev-issue.py <agent_name> [feature_description]`.

### Frontend Components
Not applicable (CLI tool).

### Backend Services
-   **Agent Discovery**: The `AgentOrchestrator` will scan the `agents/` directory on initialization to build a registry of available agents.
-   **Prompt Loading**: Each agent will be responsible for loading its own `prompt.md` file.
-   **Context Management**: The orchestrator will pass a standardized context dictionary to the agent's `execute` method. The agent then uses this context to render its Jinja2 prompt template.

## RISK ASSESSMENT
### Technical Risks
- **Refactoring Complexity**: Moving logic from `dev-issue.py` to the new architecture is a large undertaking and could introduce bugs.
  - **Mitigation**: Implement the new architecture in parallel. Keep the old script functional until the new system is stable and has feature parity. Add unit tests for the orchestrator and each new agent.
- **Prompt Management**: Having many prompt files can become hard to manage.
  - **Mitigation**: Establish clear naming conventions and a directory structure. Ensure all prompts are version-controlled in git.

### Business Risks
- **Developer Experience**: If the new system is harder to use or extend than the old script, developers may not adopt it.
  - **Mitigation**: Provide clear documentation, examples for creating new agents, and a smooth CLI experience. The goal is to make development *easier*, which should be a guiding principle.

## PROJECT DETAILS
**Estimated Effort**: 5-7 days
**Dependencies**: None, this is a foundational refactoring.
**Priority**: High
**Category**: Technical-debt / Enhancement

## ACCEPTANCE CRITERIA
- [ ] An `agents/` directory is created with at least one example agent (e.g., `feature_spec_generator`).
- [ ] An `AgentOrchestrator` class is implemented that can discover and run agents from the `agents/` directory.
- [ ] The `dev-issue.py` script is refactored to use the `AgentOrchestrator`.
- [ ] An agent's prompt is defined in a separate `.md` file and uses Jinja2 templating.
- [ ] The system can successfully generate a feature specification using the new agent-based architecture.

## GITHUB ISSUE TEMPLATE
**Title**: Refactor: Implement Modular Agent System
**Labels**: enhancement, refactor, architecture
**Assignee**:
**Project**: Core Architecture
