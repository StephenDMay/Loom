# FEATURE: LLMManager Class

## EXECUTIVE SUMMARY
This feature introduces a centralized `LLMManager` class to handle all interactions with Large Language Models (LLMs). This will abstract away the complexities of different LLM provider APIs, provide a consistent interface for the rest of the application, and manage API keys and other configuration details in a secure and organized manner.

## CODEBASE ANALYSIS
- **`agents/base_agent.py`**: The `BaseAgent` class is the abstract base class for all agents. Agents will likely be the primary consumers of the `LLMManager`. The `LLMManager` should be injectable into agents, perhaps through the `AgentOrchestrator`.
- **`agents/orchestrator.py`**: The `AgentOrchestrator` is responsible for loading and running agents. It currently instantiates agents with an `AgentConfigManager`. This is a natural place to inject an instance of the `LLMManager` into each agent.
- **`core/config_manager.py`**: The `ConfigManager` handles all configuration. The `LLMManager` will depend on it to retrieve LLM provider details, API keys, and other settings from `dev-automation.config.json`.
- **`dev-automation.config.json`**: This file contains a `llm_settings` section, which will be the source of configuration for the `LLMManager`.

## DOMAIN RESEARCH
- **User Workflows**: Developers using this system will want to easily switch between different LLM providers (e.g., Gemini, OpenAI, Anthropic) without changing their agent code. They will also want to configure model parameters like temperature, max tokens, etc., on a global or per-agent basis.
- **Industry Patterns**: It is a standard practice to have a dedicated manager or service for interacting with external services like LLMs. This promotes separation of concerns, simplifies testing (by allowing mocking of the LLM service), and makes the system more maintainable.
- **Competitive Analysis**: Many similar systems use a provider-based pattern, where there's a common interface and different concrete implementations for each LLM provider. This is a proven and effective approach.

## TECHNICAL APPROACH
The recommended approach is to create a new `LLMManager` class in a new file, `core/llm_manager.py`. This class will:
1.  Be initialized with a `ConfigManager` instance to access LLM settings.
2.  Use a factory pattern to instantiate the appropriate LLM client based on the `default_provider` setting in `dev-automation.config.json`.
3.  Provide a unified `execute_llm_call` method that takes a prompt and other parameters, and returns the LLM's response in a standardized format.
4.  Initially, we will support Gemini, with the architecture allowing for easy extension to other providers in the future.
5.  The `AgentOrchestrator` will be modified to create a single `LLMManager` instance and pass it to each agent upon initialization.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
No external API changes. A new internal Python API will be created:

**`core/llm_manager.py`**
```python
class LLMManager:
    def __init__(self, config_manager: ConfigManager):
        # ...

    def execute_llm_call(self, prompt: str, temperature: float = None) -> str:
        # ...
```

### Frontend Components
None.

### Backend Services
- **`core/llm_manager.py`**: New file containing the `LLMManager` class.
- **`agents/orchestrator.py`**: Modify to instantiate and inject the `LLMManager` into agents.
- **`agents/base_agent.py`**: Modify the `BaseAgent` constructor to accept and store an `LLMManager` instance.

## RISK ASSESSMENT
### Technical Risks
- **Provider API Changes**: LLM provider APIs can change, breaking our implementation.
  - **Mitigation**: Wrap provider-specific logic in dedicated classes and have good test coverage to quickly identify and fix breakages.
- **Configuration Complexity**: Managing configurations for multiple LLM providers can become complex.
  - **Mitigation**: Use a clear and well-documented configuration schema (`config_schema.json`) and provide sensible defaults.

### Business Risks
- **Cost Management**: Uncontrolled LLM usage can lead to high costs.
  - **Mitigation**: Implement logging and monitoring of LLM calls to track usage. Future features could include budget controls and cost estimation.
- **Vendor Lock-in**: Over-reliance on a single LLM provider.
  - **Mitigation**: The provider-based architecture of the `LLMManager` is designed to prevent this, making it easy to switch or add new providers.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to create**:
  - `core/llm_manager.py`
- **Files to modify**:
  - `agents/base_agent.py`
  - `agents/orchestrator.py`
  - `core/config_manager.py` (to add `llm_manager` to the `AgentConfigManager`)
- **Key classes/functions to implement**:
  - `core.llm_manager.LLMManager`
  - `LLMManager.execute_llm_call`
- **CLI command structure**: No CLI changes.
- **Acceptance Criteria**:
  - `LLMManager` can be instantiated.
  - `LLMManager` correctly reads LLM configuration from `ConfigManager`.
  - `LLMManager` can make a successful API call to the configured LLM provider (initially Gemini).
  - Agents receive an `LLMManager` instance and can use it to make LLM calls.

## SCOPE BOUNDARIES
**IN SCOPE**:
- A basic `LLMManager` class that can interact with a single, hard-coded LLM provider (Gemini).
- Integration of the `LLMManager` into the agent lifecycle.
- Configuration of the LLM provider via `dev-automation.config.json`.

**OUT OF SCOPE**:
- Support for multiple LLM providers at the same time.
- Caching of LLM responses.
- Advanced error handling and retry logic for LLM calls.
- Cost tracking and budget management.

## ACCEPTANCE CRITERIA
- [ ] `core/llm_manager.py` is created with a basic `LLMManager` class.
- [ ] `LLMManager` is initialized with a `ConfigManager` instance.
- [ ] `BaseAgent` is updated to accept an `LLMManager` instance in its constructor.
- [ ] `AgentOrchestrator` creates an `LLMManager` and passes it to each agent.
- [ ] A simple test can demonstrate an agent making a call through the `LLMManager`.

## GITHUB ISSUE TEMPLATE
**Title**: Create basic LLMManager class
**Labels**: feature, core
**Assignee**:
**Project**: AutoDev-Board
I will now proceed with the implementation. First, I'll create the `core/llm_manager.py` file.

