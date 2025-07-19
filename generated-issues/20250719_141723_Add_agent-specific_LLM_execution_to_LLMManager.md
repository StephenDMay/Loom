# FEATURE: Add agent-specific LLM execution to LLMManager

## EXECUTIVE SUMMARY
This feature enhances the `LLMManager` to support agent-specific LLM configurations, allowing different agents to use distinct LLM providers, models, and settings. This is crucial for the open orchestration architecture, enabling fine-grained control over the development process.

## CODEBASE ANALYSIS
- **`core/llm_manager.py`**: The central component for LLM interactions. It currently has a `_resolve_configuration` method that needs to be updated to properly merge agent-specific configurations. The `execute` method will use this resolved configuration.
- **`core/config_manager.py`**: Manages loading and accessing configuration files. The `get_agent_config` method is already implemented and can be used to fetch the merged configuration for a specific agent.
- **`agents/example_agent/agent.py`**: Demonstrates how an agent interacts with the `LLMManager`. It passes its name to the `execute` method, which is the hook for agent-specific settings.
- **`agents/example_agent/config.json`**: Contains an `llm` block with agent-specific settings. This shows the existing pattern for agent-level configuration.

The current implementation of `_resolve_configuration` in `LLMManager` is a good starting point, but it needs to be more robust in merging configurations. The `get_agent_config` in `ConfigManager` already handles the merging of the base and agent-specific `config.json` files.

## DOMAIN RESEARCH
In multi-agent systems for software development, flexibility in tool selection is paramount. Different tasks require different LLMs. For instance, a code generation agent might benefit from a model fine-tuned for code, while a documentation agent might use a model with a larger context window. This feature aligns with the core project vision of an open and flexible orchestration system.

Competitive solutions often hardcode a single LLM or provide a global setting. Allowing per-agent configuration is a significant differentiator, empowering developers to optimize their workflows for cost, performance, and quality.

## TECHNICAL APPROACH
The recommended approach is to enhance the `_resolve_configuration` method in `LLMManager`. This method should follow a clear precedence order for settings:
1.  **Explicit parameters** passed to the `execute` method (e.g., `provider`, `temperature`).
2.  **Agent-specific configuration** from the agent's `config.json`.
3.  **Global LLM settings** from the root `dev-automation.config.json`.
4.  **Hardcoded defaults** in the `LLMManager` as a final fallback.

The `ConfigManager`'s `get_agent_config` method already handles the merging of agent and global configurations, so the `LLMManager` just needs to utilize it correctly.

An alternative approach would be to have each agent instantiate its own `LLMManager` with its own configuration. This is less desirable as it would lead to redundant code and make centralized management of LLM interactions more difficult.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required.

### API Design
No changes to the external API are needed. The `execute` method of `LLMManager` will be modified internally, but its signature will remain the same.

### Frontend Components
No frontend components are affected.

### Backend Services
- **`core.llm_manager.py`**:
    - The `_resolve_configuration` method will be updated to correctly layer configurations as described in the technical approach.
    - The `execute` method will use the resolved configuration to make the LLM call.

## RISK ASSESSMENT
### Technical Risks
- **Incorrect Configuration Merging**: If the configuration precedence is not implemented correctly, it could lead to unexpected LLM behavior.
    - **Mitigation**: Add comprehensive unit tests for the `_resolve_configuration` method, covering various override scenarios.
- **Dependency on `ConfigManager`**: The `LLMManager` is tightly coupled with the `ConfigManager`.
    - **Mitigation**: This is an acceptable risk within the current architecture. The coupling is necessary for the desired functionality.

### Business Risks
- **Increased Complexity**: Adding more configuration options can make the system harder to understand for new users.
    - **Mitigation**: Provide clear documentation and examples for agent-specific LLM configuration.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to modify**:
    - `core/llm_manager.py`
    - `tests/core/test_llm_manager.py`
- **Key classes/functions to implement**:
    - `LLMManager._resolve_configuration`
    - `TestLLMManager.test_agent_specific_configuration` (new test class)
- **CLI command structure**: No changes to the CLI.
- **Acceptance criteria**:
    - When an agent calls `llm_manager.execute(prompt, agent_name='my_agent')`, the `LLMManager` should use the `llm` settings from `agents/my_agent/config.json`.
    - If an agent-specific setting is not present, the global setting from `dev-automation.config.json` should be used.
    - Explicit parameters passed to the `execute` method should override all other configurations.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Modifying `LLMManager` to use agent-specific LLM configurations.
- Adding unit tests to verify the new configuration logic.

**OUT OF SCOPE**:
- Adding new LLM providers.
- Changing the `ConfigManager` implementation.
- Implementing the API-based execution mode (it's already partially implemented, but this feature focuses on the CLI mode).

## ACCEPTANCE CRITERIA
- [ ] `LLMManager` correctly resolves agent-specific LLM provider.
- [ ] `LLMManager` correctly resolves agent-specific LLM model.
- [ ] `LLMManager` correctly resolves agent-specific temperature.
- [ ] `LLMManager` falls back to global settings when agent-specific settings are not present.
- [ ] Explicit parameters to `execute` override all other settings.
- [ ] Unit tests for `_resolve_configuration` are implemented and pass.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add agent-specific LLM execution to LLMManager
**Labels**: enhancement, core
**Assignee**:
**Project**: Loom

I will now proceed with the implementation. I will start by creating a test file to replicate the issue and then fix it.