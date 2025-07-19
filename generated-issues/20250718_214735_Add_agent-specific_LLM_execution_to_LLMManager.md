# FEATURE: Agent-Specific LLM Execution

## EXECUTIVE SUMMARY
This feature enables individual agents to specify their own LLM provider, model, and parameters within their configuration files. This provides greater flexibility and cost-optimization by allowing developers to use the best-suited model (e.g., most powerful, fastest, or cheapest) for each agent's specific task.

## CODEBASE ANALYSIS
- **`core/llm_manager.py`**: The `LLMManager` class is the central point for LLM calls. Its `execute` method currently uses a single default LLM configuration or parameters explicitly passed to it. It needs to be modified to be aware of the calling agent and resolve its specific configuration.
- **`core/config_manager.py`**: The `ConfigManager` already supports loading and merging agent-specific `config.json` files with the global `dev-automation.config.json`. The `get_agent_config(agent_name)` method provides the necessary configuration data, and no changes are expected to be needed here.
- **`agents/orchestrator.py`**: The `AgentOrchestrator` instantiates a single `LLMManager` and passes it to all agents. This workflow will remain unchanged.
- **`agents/base_agent.py`**: The `BaseAgent.execute` signature is `execute(self, llm_manager: LLMManager, config_manager: ConfigManager, agent_name: str)`. The agent already receives its own name, which it can then pass to the `LLMManager`.
- **Integration Points**: The primary integration point is the `LLMManager.execute` method. Agent implementations will be updated to pass their `agent_name` to this method.

## DOMAIN RESEARCH
- **User Workflows**: A developer creating a new agent needs a simple, declarative way to specify which LLM that agent should use. For example, a "code generation" agent might require a powerful model like GPT-4, while a "text summarization" agent could use a faster, more cost-effective model like Sonnet or Llama 3. This feature removes the need for boilerplate configuration-loading code inside each agent.
- **Industry Patterns**: In modern multi-agent frameworks (e.g., AutoGen, CrewAI), per-agent model configuration is a standard feature. It allows for task-specific optimization and is typically handled declaratively in configuration files rather than imperatively in code.
- **Competitive Solutions**: Existing frameworks typically associate an LLM configuration with each agent upon initialization or pass a context object (including agent identity) with each LLM call. Our proposed approach aligns with the latter pattern, which is more stateless and fits our current architecture.

## TECHNICAL APPROACH
The recommended approach is to modify `LLMManager.execute` to accept an optional `agent_name: str` parameter.

1.  **Modify `LLMManager.execute` Signature**: Change the method signature to include `agent_name: str = None`.
2.  **Implement Configuration Logic**: Inside `execute`, if `agent_name` is provided, use `self.config_manager.get_agent_config(agent_name)` to fetch the agent's configuration. Look for an `llm` key (e.g., `{"llm": {"provider": "openai", "model": "gpt-4-turbo"}}`) and use it to define the LLM call parameters.
3.  **Establish Override Hierarchy**: The final parameters for the LLM call will be resolved in the following order of precedence:
    1.  Explicit arguments passed directly to the `execute` method (e.g., `model="gpt-4o"`).
    2.  Agent-specific configuration from its `config.json` (if `agent_name` is passed).
    3.  Global default LLM configuration from `dev-automation.config.json`.
4.  **Update Agent Implementations**: Modify all agent classes to pass their `agent_name` to `llm_manager.execute`.
5.  **Add Unit Tests**: Create tests in `tests/core/test_llm_manager.py` to validate the new configuration resolution logic.

### Alternative Approaches
An alternative is to create a new, pre-configured `LLMManager` instance for each agent. This was rejected as it is less efficient, creating redundant objects and potentially multiple LLM clients where one would suffice. The recommended approach is cleaner and more centralized.

## IMPLEMENTATION SPECIFICATION
### Database Changes
-   None. Configuration is managed in JSON files.

### API Design
-   **`core.llm_manager.LLMManager.execute` method modification**:
    -   **New Signature**: `execute(self, prompt: str, agent_name: str = None, provider: str = None, model: str = None, temperature: float = None, max_tokens: int = None, **kwargs) -> str`
    -   The new `agent_name` parameter will drive the configuration lookup. Other arguments will serve as explicit overrides.

### Frontend Components
-   N/A. This is a backend architectural change.

### Backend Services
-   **`LLMManager`**: Will be updated to contain the configuration resolution logic based on `agent_name`.
-   **Agent Implementations (`agents/**/*.py`)**: All calls to `llm_manager.execute(...)` must be updated to `llm_manager.execute(..., agent_name=agent_name)`.

## RISK ASSESSMENT
### Technical Risks
-   **Risk 1**: Breaking change for existing agent implementations.
    -   **Mitigation**: This is a small, contained project, so a breaking change is acceptable. All agent call sites for `llm_manager.execute` must be identified and updated.
-   **Risk 2**: The configuration resolution hierarchy could be implemented incorrectly.
    -   **Mitigation**: A comprehensive set of unit tests will be created in `tests/core/test_llm_manager.py` to verify the override logic with mock agent configurations.

### Business Risks
-   **Risk 1**: Increased configuration complexity for developers.
    -   **Mitigation**: The feature will be clearly documented in the project's `README.md`, and the `example_agent` will include a clear example. The fallback to a global default ensures that simpler agents can be created without needing this configuration.

## PROJECT DETAILS
**Estimated Effort**: 1-2 days
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
-   **Files to create/modify**:
    -   `core/llm_manager.py`: Implement the core logic in the `execute` method.
    -   `agents/issue_generator/agent.py`: Update the call to `llm_manager.execute`.
    -   `agents/example_agent/agent.py`: Update the call to `llm_manager.execute`.
    -   `tests/core/test_llm_manager.py`: Add new unit tests for the feature.
    -   `agents/example_agent/config.json`: Add an example `llm` configuration block to demonstrate usage.
-   **Key classes/functions to implement**:
    -   `LLMManager.execute`: Modify to handle `agent_name` and the configuration resolution hierarchy.

## SCOPE BOUNDARIES
**IN SCOPE**:
-   Modifying `LLMManager` to read and use agent-specific `llm` configurations.
-   Updating existing agents to pass `agent_name` during execution.
-   Adding comprehensive unit tests to verify the new logic.
-   Documenting the feature for developers.

**OUT OF SCOPE**:
-   Dynamic loading/unloading of LLM clients at runtime.
-   A UI for managing agent configurations.
-   Hot-reloading of configuration changes while the application is running.

## ACCEPTANCE CRITERIA
-   [ ] `LLMManager.execute` method signature is updated to accept an optional `agent_name`.
-   [ ] `LLMManager` correctly resolves and uses LLM settings from an agent's `config.json` when `agent_name` is provided.
-   [ ] `LLMManager` falls back to the global default LLM configuration if the agent's config does not contain an `llm` section.
-   [ ] `LLMManager` prioritizes explicitly passed parameters (e.g., `model`) over agent-specific and global configurations.
-   [ ] All existing agent implementations are updated to pass `agent_name` to `llm_manager.execute`.
-   [ ] Unit tests in `test_llm_manager.py` are added to cover all configuration resolution scenarios.

## GITHUB ISSUE TEMPLATE
**Title**: feat: Add agent-specific LLM execution to LLMManager
**Labels**: feature, architecture, core
**Assignee**:
**Project**: Loom
