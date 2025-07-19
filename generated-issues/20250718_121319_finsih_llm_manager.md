# FEATURE: LLM Manager

## EXECUTIVE SUMMARY
This feature introduces a centralized "LLM Manager" to serve as a unified interface for interacting with various Large Language Models (LLMs). It abstracts away the complexities of individual model APIs, providing a consistent method for agents to make requests, which is critical for the system's core goal of supporting any AI model at any stage of development.

## CODEBASE ANALYSIS
- **Integration Point**: The `LLMManager` will be a new core component, likely residing in `core/llm_manager.py`.
- **Configuration**: It will be configured via the existing `ConfigManager`. A new `llm` section will be added to `dev-automation.config.json` and defined in `core/config_schema.json`. This will allow for global and agent-specific model configurations (e.g., API keys, model names, temperature settings).
- **Instantiation**: The `AgentOrchestrator` will be responsible for instantiating a single `LLMManager` and passing it to each agent during its initialization.
- **Usage**: `BaseAgent` will be modified to accept and store the `LLMManager` instance. Concrete agent implementations will then use this manager (e.g., `self.llm_manager.query(...)`) to perform LLM calls, instead of implementing their own API clients.
- **Technical Debt**: This refactoring will remove the need for any future agent to contain its own HTTP client or model-specific logic, thus reducing code duplication and centralizing a key dependency.

## DOMAIN RESEARCH
- **User Workflows**: Developers using this system need to easily switch between different LLMs (e.g., from `gpt-4` to `claude-3-opus` or a local model) for a given task without rewriting the agent's code. They may want to set a global default model but override it for a specific agent.
- **Industry Patterns**: A common pattern for this problem is the "Strategy" or "Adapter" design pattern. A central manager uses different "handler" or "adapter" classes for each specific API it supports. This makes the system extensible to new models by simply adding a new handler class. Libraries like LangChain and LlamaIndex use similar abstractions.
- **Competitive Analysis**: Most AI orchestration frameworks provide a model abstraction layer. Key features include standardized input/output, credential management, and support for common parameters like temperature and max tokens. Our implementation should provide these baseline features.

## TECHNICAL APPROACH
The recommended approach is to implement a `LLMManager` class that uses a dictionary of "model handlers".

1.  **`LLMManager` Class (`core/llm_manager.py`)**:
    *   Initialized with the `ConfigManager`. It reads the `llm` section of the config to find model provider settings and API keys.
    *   A `query(prompt, model_id)` method will be the primary public interface.
    *   It will maintain a registry of `BaseModelHandler` instances. When `query` is called, it will look up the appropriate handler for the `model_id` and delegate the call.

2.  **`BaseModelHandler` ABC (`core/llm_manager.py`)**:
    *   An abstract base class defining the interface for all model handlers.
    *   Will have an abstract method `query(prompt, **kwargs)` and a method to configure itself from the config.

3.  **Concrete Handlers (e.g., `OpenAIHandler`, `AnthropicHandler`)**:
    *   Implement the `BaseModelHandler` interface.
    *   Contain the logic specific to a provider's API, including request formatting, authentication, and response parsing.
    *   These will be located in a new `core/llm_handlers/` directory.

4.  **Configuration (`core/config_schema.json`)**:
    *   Add a new top-level `llm` object.
    *   This object will contain `default_model` and a `providers` dictionary where keys are provider names (e.g., "openai", "anthropic") and values are objects containing `api_key` and a list of `models`.

## IMPLEMENTATION SPECIFICATION
### Database Changes
- None.

### API Design
**`LLMManager` Class**
```python
# core/llm_manager.py
class LLMManager:
    def __init__(self, config: ConfigManager): ...
    def query(self, prompt: str, model_id: str = None, **kwargs) -> str: ...
    # model_id (e.g., "openai/gpt-4o") overrides default
```

**`BaseModelHandler` ABC**
```python
# core/llm_handlers/base.py
from abc import ABC, abstractmethod
class BaseModelHandler(ABC):
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str: ...
```

### Frontend Components
- N/A

### Backend Services
- **`AgentOrchestrator`**: Modify `load_agents` to first create an `LLMManager` instance and then pass it to the agent's constructor.
- **`BaseAgent`**: Modify `__init__` to accept and store the `llm_manager` instance.
- **New Files**:
    - `core/llm_manager.py`
    - `core/llm_handlers/base.py`
    - `core/llm_handlers/openai_handler.py`
    - `tests/core/test_llm_manager.py`

## RISK ASSESSMENT
### Technical Risks
- **Provider API Changes**: External LLM APIs can change, breaking our handlers. **Mitigation**: Pin client library versions and have robust integration tests for each handler.
- **API Key Security**: Storing API keys in config files is a risk. **Mitigation**: For initial implementation, use config files but strongly recommend using environment variables. Add documentation on best practices. Future work could involve integrating with secret managers (e.g., Vault, AWS Secrets Manager).
- **Inconsistent Error Handling**: Different models return different error formats. **Mitigation**: Handlers must normalize errors into a common exception type that the `LLMManager` can catch and propagate.

### Business Risks
- **Cost Management**: Easy access to powerful models can lead to unexpected costs. **Mitigation**: This is out of scope for the initial implementation, but the `LLMManager` is the perfect place to add logging hooks for future cost tracking features.
- **Model Dependency**: Over-reliance on a single provider. **Mitigation**: The purpose of this manager is to mitigate this exact risk by making it easy to switch providers.

## PROJECT DETAILS
**Estimated Effort**: 3-5 days
**Dependencies**: The `ConfigManager` feature must be complete and stable.
**Priority**: High
**Category**: Feature

## IMPLEMENTATION DETAILS
- **Files to Create**:
    - `core/llm_manager.py`
    - `core/llm_handlers/base.py`
    - `core/llm_handlers/openai_handler.py`
    - `tests/core/test_llm_manager.py`
- **Files to Modify**:
    - `agents/orchestrator.py`: Instantiate `LLMManager` and pass to agents.
    - `agents/base_agent.py`: Update `__init__` to accept `llm_manager`.
    - `core/config_schema.json`: Add the `llm` configuration schema.
    - `dev-automation.config.json`: Add sample `llm` configuration.
    - `requirements.txt`: Add `openai` library.
- **Key Classes/Functions**:
    - `class LLMManager`
    - `class BaseModelHandler(ABC)`
    - `class OpenAIHandler(BaseModelHandler)`
- **CLI Command Structure**: No new CLI commands. This is a backend enhancement.

## SCOPE BOUNDARIES
**IN SCOPE**:
- `LLMManager` class providing a unified `query` interface.
- Support for a default model and per-call model override.
- An initial `OpenAIHandler` for models like `gpt-4o`.
- Reading API keys from the config file.
- Modifying the orchestrator and base agent to plumb the `LLMManager` through the system.
- Unit tests for the `LLMManager` and `OpenAIHandler`.

**OUT OF SCOPE**:
- Handlers for other providers (Anthropic, Gemini, etc.) - can be added later.
- Support for local models.
- Advanced features like response streaming, function calling/tool use, or image inputs.
- Caching LLM responses.
- Cost estimation and tracking.
- A UI for managing models.

## ACCEPTANCE CRITERIA
- [ ] A new `llm` section is defined in `core/config_schema.json`.
- [ ] `LLMManager` can be initialized and loads configuration from `ConfigManager`.
- [ ] `LLMManager.query()` successfully calls the OpenAI API using a configured model and API key.
- [ ] `AgentOrchestrator` correctly initializes `LLMManager` and provides it to each loaded agent.
- [ ] An example agent can successfully use `self.llm_manager.query()` to get a result from an LLM.
- [ ] Unit tests exist for `LLMManager` that mock the model handlers and verify correct handler selection.
- [ ] An integration test exists for `OpenAIHandler` (can be disabled if API key is not present).

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Implement Core LLM Manager
**Labels**: feature, core, high-priority
**Assignee**:
**Project**: Loom MVP
```
