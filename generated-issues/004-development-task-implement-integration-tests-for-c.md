# Development Task: Implement Integration Tests for Context Management System Across Agents

## Feature Implementation Request
Implement integration tests to cover the context management system across agents, ensuring context propagation, data consistency, and error handling.

## Project Context
**Project**: Loom
**Architecture**: Agent-based architecture with an orchestrator managing the workflow between agents.
**Tech Stack**: Python, LLM (Model-Agnostic, likely Gemini), JSON configuration files, pytest.

## Implementation Specifications

### Requirements Analysis
- Extend `base_agent.py` to provide a standardized way for agents to access and modify the context.
- Modify `orchestrator.py` to inject the `ContextManager` instance into each agent during initialization.
- Create new integration tests in `tests/integration/test_context_propagation.py` to verify context propagation across agents.
- Ensure the `ContextManager` is thread-safe.
- Verify that the context is correctly used in LLM prompts via the `LLMManager`.
- Implement error handling in the `ContextManager` and add tests to verify it.

### Technical Constraints
- **Context Scope:** Global context scope.
- **Concurrency:** Handle concurrent access to the context correctly.
- **Serialization:** Consider how the context is serialized and deserialized if agents run in separate processes (though this is not currently the case).
- **Error Handling:** The context manager should handle errors gracefully.

### Integration Requirements
- **Agent Initialization:** The `orchestrator.py` needs to be modified to pass the `ContextManager` instance to each agent during initialization.
- **Context Access:** Agents will use the `context` property in `BaseAgent` to access and modify the context.
- **LLM Interaction:** The `LLMManager` should be updated to use the context when generating prompts. The integration tests should verify that the context is correctly used in the LLM prompts.

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project.
- Implement comprehensive error handling and input validation.
- Write unit tests for all new functionality.
- Document public APIs and complex business logic.
- Consider performance implications and optimization opportunities.

### Security Considerations
- Implement proper authentication and authorization checks (existing mechanisms).
- Sanitize and validate all user inputs.
- Follow secure coding practices for the technology stack.
- Consider data privacy and compliance requirements.

### Implementation Approach
1. **Analysis Phase**: Review existing codebase patterns in `agents/base_agent.py`, `agents/orchestrator.py`, `core/context_manager.py`, and `tests/integration/test_context_aware_feature_research.py`.
2. **Design Phase**: Plan the architecture for context injection and access, focusing on thread safety.
3. **Development Phase**: Implement the changes in `agents/base_agent.py`, `agents/orchestrator.py`, and `core/context_manager.py`.
4. **Testing Phase**: Write and run comprehensive integration tests in `tests/integration/test_context_propagation.py`.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [x] Modified `agents/base_agent.py` with a `context` property.
- [x] Modified `agents/orchestrator.py` to inject the `ContextManager` into agents.
- [x] Modified `core/context_manager.py` to ensure thread safety.
- [x] New integration tests in `tests/integration/test_context_propagation.py` achieving good coverage of context propagation scenarios.

### Documentation Updates
- [ ] API documentation for new methods in `BaseAgent` and `ContextManager` (if any).
- [ ] README updates if user-facing features are added.
- [ ] Architecture documentation updates if patterns change.
- [ ] Deployment or setup instruction updates if required.

### Quality Assurance
- [x] Code passes all existing tests.
- [x] New functionality is properly tested.
- [x] Code follows project style guidelines.
- [ ] Performance benchmarks are within acceptable ranges.
- [ ] Security review completed for sensitive operations.

## Success Criteria
- Agents can access and modify the shared context.
- Context is correctly propagated between agents during orchestration.
- The `ContextManager` is thread-safe and handles concurrent access correctly.
- Integration tests cover various context propagation scenarios.
- LLM prompts are correctly informed by the context.
- Error handling is implemented and tested in the `ContextManager`.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Detailed Implementation Steps:**

1.  **Modify `agents/base_agent.py`:**
    *   Add a `context` property to the `BaseAgent` class. This property should provide access to the injected `ContextManager` instance.

    ```python
    from abc import ABC, abstractmethod

    class BaseAgent(ABC):
        def __init__(self, config, context=None): # Add context parameter
            self.config = config
            self._context = context # Store the context
            super().__init__()

        @property
        def context(self):
            return self._context

        @abstractmethod
        def run(self, *args, **kwargs):
            pass
    
2.  **Modify `agents/orchestrator.py`:**
    *   Import the `ContextManager` class.
    *   Create a single instance of the `ContextManager` in the `Orchestrator` class.
    *   Modify the agent initialization logic to inject the `ContextManager` instance into each agent.

    ```python
    from core.context_manager import ContextManager

    class Orchestrator:
        def __init__(self, agent_configs):
            self.context_manager = ContextManager() # Create a single context manager
            self.agents = {}
            for agent_name, config in agent_configs.items():
                agent_class = self._load_agent_class(config["class_name"])
                self.agents[agent_name] = agent_class(config, context=self.context_manager) # Inject context
    
3.  **Modify `core/context_manager.py`:**
    *   Implement thread-safe context management using a `threading.Lock`.

    ```python
    import threading

    class ContextManager:
        def __init__(self):
            self._context = {}
            self._lock = threading.Lock()

        def get(self, key):
            with self._lock:
                return self._context.get(key)

        def set(self, key, value):
            with self._lock:
                self._context[key] = value

        def update(self, data: dict):
            with self._lock:
                self._context.update(data)
    
4.  **Create `tests/integration/test_context_propagation.py`:**
    *   Create integration tests to verify context propagation between agents.  This will require setting up a simplified agent workflow.  The tests should:
        *   Initialize the `Orchestrator` with a mock configuration.
        *   Verify that agents can access the context.
        *   Verify that modifying the context in one agent affects subsequent agents.
        *   Test concurrent access to the context.
        *   Test error handling scenarios (e.g., attempting to access a non-existent key).

    ```python
    import pytest
    from agents.orchestrator import Orchestrator
    from agents.base_agent import BaseAgent
    from core.context_manager import ContextManager
    import threading
    import time
    from unittest.mock import MagicMock

    class MockAgent(BaseAgent):
        def __init__(self, config, context=None):
            super().__init__(config, context)

        def run(self, input_data):
            if self.config['action'] == 'set':
                self.context.set(self.config['key'], self.config['value'])
            elif self.config['action'] == 'get':
                return self.context.get(self.config['key'])
            elif self.config['action'] == 'update':
                self.context.update(self.config['data'])
            return None

    @pytest.fixture
    def orchestrator():
        agent_configs = {
            "agent1": {"class_name": "MockAgent", "action": "set", "key": "test_key", "value": "test_value"},
            "agent2": {"class_name": "MockAgent", "action": "get", "key": "test_key"},
            "agent3": {"class_name": "MockAgent", "action": "update", "data": {"key1": "value1", "key2": "value2"}}
        }
        # Mock the _load_agent_class method to return MockAgent
        orchestrator = Orchestrator(agent_configs)
        orchestrator._load_agent_class = MagicMock(return_value=MockAgent)
        orchestrator.__init__ = MagicMock(return_value=None)
        orchestrator.agents = {name: MockAgent(config, orchestrator.context_manager) for name, config in agent_configs.items()}
        orchestrator.context_manager = ContextManager()
        return orchestrator

    def test_context_propagation(orchestrator):
        # Simulate running agents in sequence
        orchestrator.agents["agent1"].run(None)
        value = orchestrator.agents["agent2"].run(None)
        assert value == "test_value"
        orchestrator.agents["agent3"].run(None)
        assert orchestrator.context_manager.get("key1") == "value1"
        assert orchestrator.context_manager.get("key2") == "value2"

    def test_concurrent_context_access(orchestrator):
        def set_context(agent_name, key, value):
            orchestrator.agents[agent_name].config['action'] = 'set'
            orchestrator.agents[agent_name].config['key'] = key
            orchestrator.agents[agent_name].config['value'] = value
            orchestrator.agents[agent_name].run(None)

        threads = []
        for i in range(5):
            thread = threading.Thread(target=set_context, args=(f"agent{i+1}", f"key{i}", f"value{i}"))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for i in range(5):
            assert orchestrator.context_manager.get(f"key{i}") == f"value{i}"
    
5.  **Update `tests/core/test_context_manager.py`:**
    *   Add tests to specifically verify the thread-safety of the `ContextManager`.

    ```python
    import pytest
    from core.context_manager import ContextManager
    import threading

    def test_context_manager_thread_safety():
        context_manager = ContextManager()
        num_threads = 10
        num_iterations = 100

        def update_context(thread_id):
            for i in range(num_iterations):
                key = f"key_{thread_id}_{i}"
                value = f"value_{thread_id}_{i}"
                context_manager.set(key, value)
                assert context_manager.get(key) == value

        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=update_context, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Basic verification that all threads wrote *something*
        total_keys = 0
        for i in range(num_threads):
            for j in range(num_iterations):
                key = f"key_{i}_{j}"
                if context_manager.get(key) is not None:
                    total_keys += 1
        assert total_keys == num_threads * num_iterations
    
6.  **LLM Interaction Testing:**
    *   Modify or create a new integration test to verify that the `LLMManager` correctly uses the context when generating prompts. This will likely involve mocking the LLM to verify the prompt content.

    ```python
    # Example (requires adaptation to existing LLMManager tests)
    def test_llm_manager_uses_context(orchestrator, mocker):
        # Assuming you have an LLMManager instance in your orchestrator
        llm_manager = orchestrator.agents["agent1"].llm_manager # Assuming agent1 has access to llm_manager
        context_key = "llm_test_key"
        context_value = "llm_test_value"
        orchestrator.context_manager.set(context_key, context_value)

        # Mock the LLM's generate method
        mock_llm_generate = mocker.patch.object(llm_manager, 'generate')
        mock_llm_generate.return_value = "LLM Response"

        # Run an agent that uses the LLM
        orchestrator.agents["agent1"].run({"prompt": "Test prompt"})

        # Assert that the LLM was called with a prompt that includes the context
        mock_llm_generate.assert_called_once()
        call_args = mock_llm_generate.call_args
        prompt_used = call_args[0][0]  # Assuming prompt is the first argument
        assert context_value in prompt_used
    
These steps provide a comprehensive guide to implementing integration tests for the context management system across agents. Remember to adapt the code examples to fit the specific structure and requirements of the Loom project.