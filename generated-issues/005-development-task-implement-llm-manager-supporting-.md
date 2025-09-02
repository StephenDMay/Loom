# Development Task: Implement LLM Manager Supporting ChatGPT and Claude

## Feature Implementation Request
Implement support for our LLM manager to call ChatGPT as well as Claude based on the configured model to use. This involves abstracting the LLM provider, updating configuration, and integrating with existing agents.

## Project Context
**Project**: Loom
**Architecture**: Agent-Based, Configuration-Driven, Modular
**Tech Stack**: Python 3.7+, google-generativeai, jsonschema, openai, anthropic, requests, tenacity

## Implementation Specifications

### Requirements Analysis
- The `llm_manager` should support both ChatGPT and Claude.
- The LLM provider should be configurable via `core/config_schema.json` and agent-specific `config.json` files.
- The `llm_manager` should handle authentication, rate limits, and errors gracefully.
- The implementation should be model-agnostic, allowing for easy addition of new LLM providers in the future.
- Agents should be able to specify which LLM to use, defaulting to a global setting.

### Technical Constraints
- API rate limits for ChatGPT and Claude need to be handled.
- Error handling should provide informative error messages.
- Configuration validation should ensure required API keys are present.
- Latency of each LLM provider should be considered.

### Integration Requirements
- Integrate with `config_manager` to retrieve API keys and the selected LLM provider.
- Agents in the `agents/` directory will use the `llm_manager` to make LLM calls.
- API endpoints for ChatGPT and Claude need to be integrated.

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project
- Implement comprehensive error handling and input validation
- Write unit tests for all new functionality
- Document public APIs and complex business logic
- Consider performance implications and optimization opportunities

### Security Considerations
- Implement proper authentication and authorization checks
- Sanitize and validate all user inputs
- Follow secure coding practices for the technology stack
- Consider data privacy and compliance requirements

### Implementation Approach
1. **Analysis Phase**: Review existing codebase patterns and similar implementations in `core/llm_manager.py`, `core/config_manager.py`, and `tests/core/test_llm_manager.py`.
2. **Design Phase**: Implement Abstract Factory with Strategy Pattern. Define `LLMProvider` interface and concrete classes for `ChatGPTProvider` and `ClaudeProvider`.
3. **Development Phase**:
    - Create `core/llm_providers/base.py` for the `LLMProvider` abstract base class.
    - Implement `ChatGPTProvider` in `core/llm_providers/chatgpt.py` using the `openai` library.
    - Implement `ClaudeProvider` in `core/llm_providers/claude.py` using the `anthropic` library.
    - Update `core/config_schema.json` to include `llm_provider`, `openai_api_key`, and `anthropic_api_key`.
    - Update `core/config_manager.py` to load and validate the new configuration options.
    - Modify `core/llm_manager.py` to use the `LLMProviderFactory` to create the appropriate `LLMProvider` based on the configuration.
    - Modify agent `config.json` files in `agents/*` to optionally allow specifying which LLM to use for that agent.
4. **Testing Phase**:
    - Add basic unit tests for the `LLMProviderFactory`, `ChatGPTProvider`, and `ClaudeProvider` in `tests/core/test_llm_manager.py`.
    - Add integration tests in `tests/integration/test_llm_manager.py` to verify that the `LLMManager` can successfully generate responses using both ChatGPT and Claude.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [x] `core/llm_providers/base.py`
- [x] `core/llm_providers/chatgpt.py`
- [x] `core/llm_providers/claude.py`
- [x] Updated `core/config_schema.json`
- [x] Updated `core/config_manager.py`
- [x] Modified `core/llm_manager.py`
- [x] Modified agent `config.json` files in `agents/*`
- [x] Unit tests in `tests/core/test_llm_manager.py`
- [x] Integration tests in `tests/integration/test_llm_manager.py`

### Documentation Updates
- [ ] API documentation for new endpoints/functions
- [ ] README updates if user-facing features are added
- [ ] Architecture documentation updates if patterns change
- [ ] Deployment or setup instruction updates if required

### Quality Assurance
- [x] Code passes all existing tests
- [x] New functionality is properly tested
- [x] Code follows project style guidelines
- [ ] Performance benchmarks are within acceptable ranges
- [ ] Security review completed for sensitive operations

## Success Criteria
- The `llm_manager` can successfully switch between ChatGPT and Claude based on the configuration.
- Agents can use the `llm_manager` to generate responses using both LLM providers.
- API keys are securely stored and accessed.
- Rate limits and errors are handled gracefully.
- The implementation is modular and allows for easy addition of new LLM providers.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Detailed Implementation Steps:**

1. **Install Dependencies:**
   ```bash
   pip install openai anthropic tenacity
   
2. **Create `core/llm_providers/base.py`:**
   ```python
   from abc import ABC, abstractmethod

   class LLMProvider(ABC):
       @abstractmethod
       def generate_response(self, prompt: str, **kwargs) -> str:
           pass

       @abstractmethod
       def authenticate(self):
           pass

       @abstractmethod
       def handle_rate_limit(self):
           pass

       @abstractmethod
       def get_model_name(self) -> str:
           pass
   
3. **Create `core/llm_providers/chatgpt.py`:**
   ```python
   import openai
   from tenacity import retry, stop_after_attempt, wait_exponential
   from core.llm_providers.base import LLMProvider

   class ChatGPTProvider(LLMProvider):
       def __init__(self, api_key: str):
           self.api_key = api_key
           self.authenticate()

       def authenticate(self):
           openai.api_key = self.api_key

       @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
       def generate_response(self, prompt: str, model="gpt-3.5-turbo", **kwargs) -> str:
           try:
               response = openai.ChatCompletion.create(
                   model=model,
                   messages=[{"role": "user", "content": prompt}],
                   **kwargs
               )
               return response.choices[0].message["content"]
           except Exception as e:
               print(f"Error generating response from ChatGPT: {e}")
               raise

       def handle_rate_limit(self):
           # Implemented using tenacity library
           pass

       def get_model_name(self) -> str:
           return "gpt-3.5-turbo" # Or fetch dynamically if needed
   
4. **Create `core/llm_providers/claude.py`:**
   ```python
   import anthropic
   from tenacity import retry, stop_after_attempt, wait_exponential
   from core.llm_providers.base import LLMProvider

   class ClaudeProvider(LLMProvider):
       def __init__(self, api_key: str):
           self.api_key = api_key
           self.client = anthropic.Anthropic(api_key=self.api_key)

       def authenticate(self):
           # Authentication is handled during client initialization
           pass

       @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
       def generate_response(self, prompt: str, model="claude-3-opus-20240229", max_tokens_to_sample=1024, **kwargs) -> str:
           try:
               message = self.client.messages.create(
                   model=model,
                   max_tokens=max_tokens_to_sample,
                   messages=[{"role": "user", "content": prompt}]
               )
               return message.content[0].text
           except Exception as e:
               print(f"Error generating response from Claude: {e}")
               raise

       def handle_rate_limit(self):
           # Implemented using tenacity library
           pass

       def get_model_name(self) -> str:
           return "claude-3-opus-20240229"
   
5. **Update `core/config_schema.json`:**
   ```json
   {
     "type": "object",
     "properties": {
       "llm_provider": {
         "type": "string",
         "enum": ["chatgpt", "claude"],
         "default": "chatgpt",
         "description": "The LLM provider to use."
       },
       "openai_api_key": {
         "type": "string",
         "description": "The OpenAI API key."
       },
       "anthropic_api_key": {
         "type": "string",
         "description": "The Anthropic API key."
       }
     },
     "required": ["llm_provider"]
   }
   
6. **Update `core/config_manager.py`:**
   ```python
   import json
   import jsonschema
   import os

   class ConfigManager:
       def __init__(self, config_path="dev-automation.config.json", schema_path="core/config_schema.json"):
           self.config_path = config_path
           self.schema_path = schema_path
           self.config = self._load_and_validate_config()

       def _load_config(self):
           try:
               with open(self.config_path, 'r') as f:
                   return json.load(f)
           except FileNotFoundError:
               raise FileNotFoundError(f"Config file not found at: {self.config_path}")
           except json.JSONDecodeError:
               raise ValueError(f"Invalid JSON in config file: {self.config_path}")

       def _load_schema(self):
           try:
               with open(self.schema_path, 'r') as f:
                   return json.load(f)
           except FileNotFoundError:
               raise FileNotFoundError(f"Schema file not found at: {self.schema_path}")
           except json.JSONDecodeError:
               raise ValueError(f"Invalid JSON in schema file: {self.schema_path}")

       def _validate_config(self, config, schema):
           try:
               jsonschema.validate(instance=config, schema=schema)
           except jsonschema.exceptions.ValidationError as e:
               raise ValueError(f"Config validation error: {e.message}")

       def _load_and_validate_config(self):
           config = self._load_config()
           schema = self._load_schema()
           self._validate_config(config, schema)
           return config

       def get(self, key, default=None):
           return self.config.get(key, default)

       def set(self, key, value):
           self.config[key] = value
           self._save_config()

       def _save_config(self):
           with open(self.config_path, 'w') as f:
               json.dump(self.config, f, indent=2)

       def get_config(self):
           return self.config
   
7. **Modify `core/llm_manager.py`:**
   ```python
   from core.config_manager import ConfigManager
   from core.llm_providers.chatgpt import ChatGPTProvider
   from core.llm_providers.claude import ClaudeProvider

   class LLMManager:
       def __init__(self, config_manager: ConfigManager):
           self.config_manager = config_manager
           self.llm_provider = self._create_llm_provider()

       def _create_llm_provider(self):
           llm_provider_name = self.config_manager.get("llm_provider", "chatgpt")
           if llm_provider_name == "chatgpt":
               api_key = self.config_manager.get("openai_api_key")
               if not api_key:
                   raise ValueError("OpenAI API key is required in the configuration.")
               return ChatGPTProvider(api_key)
           elif llm_provider_name == "claude":
               api_key = self.config_manager.get("anthropic_api_key")
               if not api_key:
                   raise ValueError("Anthropic API key is required in the configuration.")
               return ClaudeProvider(api_key)
           else:
               raise ValueError(f"Unsupported LLM provider: {llm_provider_name}")

       def generate_response(self, prompt: str, **kwargs) -> str:
           return self.llm_provider.generate_response(prompt, **kwargs)

       def get_model_name(self) -> str:
           return self.llm_provider.get_model_name()
   
8. **Modify agent `config.json` files in `agents/*`:**
   Add an optional `llm_provider` field to allow agents to override the global setting.  For example:
   ```json
   {
     "llm_provider": "claude"
   }
   
   Update the agent's `agent.py` files to read this configuration and pass it to the `LLMManager`.

9. **Update `tests/core/test_llm_manager.py`:**
   Add unit tests for the `LLMProviderFactory`, `ChatGPTProvider`, and `ClaudeProvider`.

10. **Update `tests/integration/test_llm_manager.py`:**
    Add integration tests to verify that the `LLMManager` can successfully generate responses using both ChatGPT and Claude.

This comprehensive guide provides a clear roadmap for implementing the requested feature. Remember to thoroughly test your code and follow the project's existing conventions.