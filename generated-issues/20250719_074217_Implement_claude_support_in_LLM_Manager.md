# FEATURE: Implement Claude Support in LLM Manager

## EXECUTIVE SUMMARY
This feature adds support for Anthropic's Claude family of models (Haiku, Sonnet, Opus) to the central LLM Manager. This enhances the system's flexibility, allowing developers to leverage Claude's unique capabilities, such as its large context window and strong reasoning skills, directly within their automated workflows.

## CODEBASE ANALYSIS
The existing `LLMManager` is built on an open orchestration architecture, presumably using a provider/adapter pattern. We expect a `BaseLLMProvider` abstract base class and at least one existing implementation (e.g., `OpenAIProvider`).

- **Integration Points**:
    1.  **Provider Factory**: A factory function likely exists in `llm_manager/factory.py` that instantiates providers based on a configuration string (e.g., "openai", "claude"). This will need to be updated to recognize "claude".
    2.  **Configuration**: The system's configuration loader (e.g., loading `config.yaml` or environment variables) will need to read `ANTHROPIC_API_KEY`.
    3.  **Core Logic**: Any service calling the `LLMManager` will now be able to pass in a Claude model name (e.g., `claude-3-opus-20240229`). No changes should be needed in the calling services if the `LLMManager` interface is consistent.

- **Impact Assessment**: The impact on existing systems is low, as this is an additive change. The new `ClaudeProvider` will be isolated, and no existing provider logic will be modified.

- **Technical Debt**: If a `BaseLLMProvider` interface does not exist and the system is hardcoded for a single provider (e.g., OpenAI), this work will be blocked. A refactoring task to create the provider abstraction must be completed first. This specification assumes the abstraction exists.

## DOMAIN RESEARCH
- **User Workflows**: A developer wants to use Claude 3 Opus for a complex code generation task. They will update their project's `config.yaml` to specify a Claude model and provide the API key. The system should then route the relevant generation tasks to the Claude API without requiring any code changes from the user.

- **Industry Patterns**: Leading tools like LangChain and LiteLLM use an adapter pattern. They create a specific client class for each LLM provider that conforms to a unified interface. This is the best practice we will follow. A key challenge is handling provider-specific nuances, such as:
    - **System Prompts**: The new Anthropic Messages API handles system prompts differently than OpenAI. It should be passed as a top-level `system` parameter.
    - **Parameter Naming**: `max_tokens` is now standard in the Messages API, but older Anthropic models used `max_tokens_to_sample`. We will target the modern Messages API.
    - **Error Handling**: Anthropic has its own set of API error codes that need to be caught and translated into generic system exceptions where possible.

- **Competitive Analysis**: LiteLLM provides a robust translation layer that handles these differences automatically. We will implement a similar, tailored version for our system, focusing on translating our internal standard message format to the Anthropic Messages API format.

## TECHNICAL APPROACH
The recommended approach is to create a new `ClaudeProvider` class that inherits from `BaseLLMProvider` and encapsulates all interaction with the Anthropic API using their official Python SDK.

1.  **Add Dependency**: Add the `anthropic` Python library to `pyproject.toml` or `requirements.txt`.
2.  **Create Provider**: Implement `llm_manager/providers/claude_provider.py`. This class will:
    - Initialize by reading the `ANTHROPIC_API_KEY` from the system's configuration service.
    - Implement the required `generate_response(messages, model, **kwargs)` method from the base class.
    - Inside `generate_response`, transform the system's internal message list into the format required by `anthropic.messages.create()`. This includes separating the system prompt from the user/assistant messages.
    - Map common parameters like `temperature` and `max_tokens` to the Anthropic API call.
    - Invoke the API and parse the `Message` response object to extract the content.
    - Wrap API calls in `try...except` blocks to handle `anthropic.APIError` exceptions and raise standardized system errors.
3.  **Update Factory**: Modify the provider factory to instantiate `ClaudeProvider` when the model name indicates a Claude model.

**Alternative Approach**: Use a third-party abstraction library like LiteLLM internally within our `LLMManager`. This would speed up initial implementation but adds a significant external dependency and reduces our control over a core part of the system. Given the strategic importance of the LLM orchestration layer, building a native provider is preferred.

## IMPLEMENTATION SPECIFICATION
### Database Changes
- None. This feature is stateless and does not require schema modifications.

### API Design
- No changes to external-facing APIs.
- The internal Python API of the `LLMManager` remains the same:
  ```python
  # No change for consumers of the manager
  llm_manager.generate_response(
      model="claude-3-opus-20240229",
      messages=[{"role": "user", "content": "Hello!"}]
  )
  ```

### Frontend Components
- None. This is a backend-only feature.

### Backend Services
- **`llm_manager/providers/claude_provider.py` (New File)**:
    - `ClaudeProvider(BaseLLMProvider)` class.
    - `__init__(self)`: Initializes `anthropic.Anthropic(api_key=...)`.
    - `generate_response(self, messages, model, **kwargs)`: Core logic for API interaction.
    - `_prepare_api_request(self, messages, model, **kwargs)`: Private helper to format the request payload.
- **`llm_manager/factory.py` (Modification)**:
    - Update the factory function to include a case for Claude models.
      ```python
      # Example logic
      def get_provider(model_name: str) -> BaseLLMProvider:
          if "claude" in model_name:
              return ClaudeProvider()
          elif "gpt" in model_name:
              return OpenAIProvider()
          # ...
      ```
- **`config/settings.py` (Modification)**:
    - Add logic to load `ANTHROPIC_API_KEY` from environment variables or a secrets management service.

## RISK ASSESSMENT
### Technical Risks
- **Provider Interface Incompatibility**: The `BaseLLMProvider` interface may lack a way to handle Claude-specific features (e.g., tool use format).
  - **Mitigation**: For this initial implementation, we will only support text generation. The interface can be extended in a future task if more advanced features are needed.
- **API Rate Limiting**: Aggressive polling or large-scale use could hit Anthropic's API rate limits.
  - **Mitigation**: The `ClaudeProvider` should catch rate limit errors (`anthropic.RateLimitError`) and implement an exponential backoff and retry mechanism.

### Business Risks
- **Cost Overruns**: Claude 3 Opus is a premium model. Unmonitored use could lead to unexpected costs.
  - **Mitigation**: Clearly document the cost implications. Add warnings in the documentation and consider implementing a cost estimation feature in a subsequent task.
- **Output Consistency**: Claude's output style may differ from existing models, potentially affecting downstream tools that parse the markdown output.
  - **Mitigation**: This is an inherent challenge of a multi-model system. We will accept native model output for now. Future work could involve a "normalization" layer if consistency becomes a major issue.

## PROJECT DETAILS
**Estimated Effort**: 4 days
- Research & Setup: 0.5 days
- `ClaudeProvider` Implementation: 1.5 days
- Unit & Integration Testing: 1.5 days
- Documentation & PR Review: 0.5 days

**Dependencies**:
- A pre-existing and well-defined `BaseLLMProvider` abstract class.
- Access to an Anthropic developer API key for integration testing.

**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to Create**:
    - `llm_manager/providers/claude_provider.py`
    - `tests/providers/test_claude_provider.py`
- **Files to Modify**:
    - `llm_manager/factory.py` (or equivalent provider router)
    - `config/settings.py` (or equivalent config loader)
    - `pyproject.toml` or `requirements.txt` (to add `anthropic`)
    - `README.md` or `docs/llms.md` (to document the new provider)
- **Key Classes/Functions**:
    - `class ClaudeProvider(BaseLLMProvider)`
    - `def generate_response(self, ...)`: Must handle the `system` prompt parameter separately from the `messages` list when calling the Anthropic API.
- **CLI Command Structure**: Not applicable. This is a library feature.
- **Acceptance Criteria for "Done"**:
    - A developer can configure the system with an `ANTHROPIC_API_KEY`.
    - Calling the `LLMManager` with a model name like `"claude-3-sonnet-20240229"` successfully returns a response from the Anthropic API.
    - Unit tests for `ClaudeProvider` exist with >90% code coverage, mocking the external API.
    - An integration test exists that makes a real (but small) API call to Claude Haiku.
    - Documentation is updated to reflect Claude support.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Support for text generation via the Anthropic Messages API (`messages.create`).
- Support for `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, and `claude-3-haiku-20240307`.
- Handling of `temperature` and `max_tokens` parameters.
- Basic error handling for common API errors (authentication, rate limiting).
- Securely loading the `ANTHROPIC_API_KEY` from the environment.

**OUT OF SCOPE**:
- Streaming responses. (To be handled in a separate feature).
- Support for Claude's tool use / function calling capabilities. (Requires interface extension).
- Image/vision capabilities.
- A UI for selecting models or managing API keys.
- Cost tracking and budget controls.

## ACCEPTANCE CRITERIA
- [ ] `ClaudeProvider` is implemented and inherits from `BaseLLMProvider`.
- [ ] The provider factory correctly instantiates `ClaudeProvider` for models with "claude" in their name.
- [ ] The system correctly loads `ANTHROPIC_API_KEY` from environment variables.
- [ ] A call to `llm_manager.generate_response(model="claude-3-haiku-20240307", ...)` successfully returns a text completion.
- [ ] The implementation correctly separates the system prompt into the `system` parameter of the Anthropic API call.
- [ ] `anthropic.APIError` and its subclasses are caught and handled gracefully.
- [ ] Unit tests for `ClaudeProvider` are written and pass.
- [ ] Documentation is updated to explain how to configure and use Claude models.

## GITHUB ISSUE TEMPLATE
**Title**: feat: Implement Anthropic Claude provider in LLM Manager
**Labels**: `feature`, `llm-integration`, `backend`
**Assignee**:
**Project**: Core Features