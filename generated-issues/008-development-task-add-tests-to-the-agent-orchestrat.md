# Development Task: Add Tests to the Agent Orchestrator

## Feature Implementation Request
Implement comprehensive tests for the agent orchestrator to ensure its reliability, maintainability, and scalability. The tests should cover core functionality, error handling, and integration with other components like agents, LLM manager, and context manager.

## Project Context
**Project**: loom
**Architecture**: Agent-Based Architecture, Configuration-Driven, Context Passing
**Tech Stack**: Python 3.7+, Google Gemini (using `google-generativeai`), Custom configuration management using JSON files and `core/config_manager.py`, `pytest`

## Implementation Specifications

### Requirements Analysis
1.  **Unit Tests:** Test individual components of the orchestrator in isolation, mocking dependencies like `BaseAgent`, `LLMManager`, `ConfigManager`, and `ContextManager`.
2.  **Integration Tests:** Verify the interaction between the orchestrator and real agent implementations, using simplified configurations for predictable behavior.
3.  **Error Handling Tests:** Simulate agent failures (e.g., exceptions, timeouts) and verify that the orchestrator handles them gracefully, logs them, and potentially retries failed agents.
4.  **Logging Tests:** Verify that the orchestrator logs important events, such as agent start/end, errors, and context updates.
5.  **End-to-End Tests:** Simulate complete workflows, starting from an initial request and verifying the final output.
6.  **Code Coverage:** Aim for a minimum of 80% code coverage.

### Technical Constraints
1.  **Asynchronous Operations:** The orchestrator might use asynchronous operations (async/await) for parallel agent execution. Tests need to handle asynchronous code correctly.
2.  **Error Handling:** The orchestrator needs to handle errors from individual agents gracefully. Tests should verify that the orchestrator catches and logs exceptions, and potentially retries failed agents.
3.  **Logging:** The orchestrator likely uses logging for debugging and monitoring. Tests should verify that the orchestrator logs important events, such as agent start/end, errors, and context updates.
4.  **Concurrency:** If the orchestrator supports concurrent agent execution, tests need to ensure thread safety and prevent race conditions.
5.  **LLM Unpredictability:** LLM responses can be unpredictable, making it difficult to write deterministic tests. Mock the `LLMManager` and provide predefined LLM responses for testing purposes.

### Integration Requirements
1.  **Agents:** The orchestrator interacts with agents through the `BaseAgent` interface. Tests need to mock or use real agent implementations.
2.  **LLM Manager:** The orchestrator uses the `LLMManager` to interact with LLMs. Tests need to mock the `LLMManager` to control the LLM responses.
3.  **Configuration Manager:** The orchestrator uses the `ConfigManager` to load agent configurations. Tests need to provide test configurations.
4.  **Context Manager:** The orchestrator uses the `ContextManager` to manage the context passed between agents. Tests need to verify that the context is correctly updated and passed.
5.  **Logging:** The orchestrator uses the logging module to log events. Tests need to verify that the correct events are logged.

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project.
- Implement comprehensive error handling and input validation.
- Write unit tests for all new functionality.
- Document public APIs and complex business logic.
- Consider performance implications and optimization opportunities.

### Security Considerations
- N/A

### Implementation Approach
1.  **Analysis Phase**: Review existing tests in `tests/agents/test_orchestrator.py` and `tests/core/test_orchestrator_logging.py`, as well as the orchestrator code in `agents/orchestrator.py`.
2.  **Design Phase**: Plan the tests based on the requirements analysis, focusing on unit, integration, and error handling.
3.  **Development Phase**: Implement the tests using `pytest` and `unittest.mock` or `pytest-mock`.
4.  **Testing Phase**: Run the tests and ensure they pass. Use `pytest-cov` to check code coverage.
5.  **Documentation Phase**: Add comments to the tests to explain their purpose.

## Expected Deliverables

### Code Artifacts
-   [x] Modified `tests/agents/test_orchestrator.py` with new unit and integration tests.
-   [x] Potentially modified `tests/core/test_orchestrator_logging.py` with new logging tests.
-   [x] Mock objects for dependencies like `BaseAgent`, `LLMManager`, `ConfigManager`, and `ContextManager`.

### Documentation Updates
-   [ ] Add comments to the tests to explain their purpose.

### Quality Assurance
-   [x] Code passes all existing tests.
-   [x] New functionality is properly tested.
-   [x] Code follows project style guidelines.
-   [x] Minimum 80% code coverage is achieved.

## Success Criteria
1.  Comprehensive test suite for the agent orchestrator.
2.  High code coverage (minimum 80%).
3.  Tests cover core functionality, error handling, and integration with other components.
4.  Tests are well-documented and easy to understand.
5.  The orchestrator is more reliable, maintainable, and scalable.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Implementation Steps:**

1.  **Set up test environment:** Ensure `pytest`, `pytest-mock`, and `pytest-cov` are installed.
2.  **Create unit tests:**
    *   Test agent instantiation by mocking `ConfigManager` and verifying that the orchestrator creates agents with the correct classes. (See example in Research Report)
    *   Test context passing by mocking agents and verifying that the context is updated correctly after each agent execution.
    *   Test the orchestrator's main loop by mocking agents and verifying that they are executed in the correct order.
3.  **Create integration tests:**
    *   Use a simplified agent implementation (like `MockAgent` in the Research Report) to test the interaction between the orchestrator and agents.
    *   Verify that the orchestrator correctly calls the `execute()` method on agents and handles the returned results.
4.  **Create error handling tests:**
    *   Use a `FailingAgent` (like in the Research Report) to simulate agent failures.
    *   Verify that the orchestrator catches exceptions, logs them, and potentially retries failed agents.
5.  **Create logging tests:**
    *   Use `caplog` fixture in `pytest` to capture log messages.
    *   Verify that the orchestrator logs important events, such as agent start/end, errors, and context updates.
6.  **Run tests and check code coverage:**
    *   Run `pytest` to execute the tests.
    *   Run `pytest --cov=agents --cov-report term-missing` to check code coverage.
    *   Address any uncovered areas by adding new tests.
7.  **Commit changes:** Commit the changes to `tests/agents/test_orchestrator.py` and potentially `tests/core/test_orchestrator_logging.py`.

**Example Code (from Research Report):**

*   **Unit Test (Agent Instantiation):**
    ```python
    from unittest.mock import MagicMock
    from agents.orchestrator import AgentOrchestrator

    def test_orchestrator_instantiates_agents():
        config_manager_mock = MagicMock()
        config_manager_mock.get_agent_configs.return_value = [
            {"name": "test_agent", "module": "agents.example_agent.agent", "class_name": "ExampleAgent", "config": {}}
        ]
        orchestrator = AgentOrchestrator(config_manager=config_manager_mock, llm_manager=MagicMock(), context_manager=MagicMock())
        orchestrator.load_agents()
        assert len(orchestrator.agents) == 1
        assert orchestrator.agents["test_agent"].__class__.__name__ == "ExampleAgent"
    
*   **Integration Test (Agent Execution):**
    ```python
    import pytest
    from agents.orchestrator import AgentOrchestrator
    from agents.base_agent import BaseAgent

    class MockAgent(BaseAgent):
        def __init__(self, name, config, llm_manager, context_manager):
            super().__init__(name, config, llm_manager, context_manager)
        async def execute(self, feature_request, context):
            return "Mock Agent Result", context

    @pytest.fixture
    def orchestrator(mocker):
        config_manager_mock = mocker.MagicMock()
        config_manager_mock.get_agent_configs.return_value = [
            {"name": "mock_agent", "module": __name__, "class_name": "MockAgent", "config": {}}
        ]
        llm_manager_mock = mocker.MagicMock()
        context_manager_mock = mocker.MagicMock()
        orchestrator = AgentOrchestrator(config_manager=config_manager_mock, llm_manager=llm_manager_mock, context_manager=context_manager_mock)
        orchestrator.load_agents()
        return orchestrator

    @pytest.mark.asyncio
    async def test_orchestrator_executes_agent(orchestrator):
        feature_request = "Test Feature"
        context = {}
        results = await orchestrator.execute_agents(feature_request, context)
        assert "mock_agent" in results
        assert results["mock_agent"] == "Mock Agent Result"
    
*   **Error Handling Test:**
    ```python
    import pytest
    from unittest.mock import MagicMock
    from agents.orchestrator import AgentOrchestrator
    from agents.base_agent import BaseAgent

    class FailingAgent(BaseAgent):
        def __init__(self, name, config, llm_manager, context_manager):
            super().__init__(name, config, llm_manager, context_manager)
        async def execute(self, feature_request, context):
            raise Exception("Agent failed")

    @pytest.fixture
    def orchestrator(mocker):
        config_manager_mock = mocker.MagicMock()
        config_manager_mock.get_agent_configs.return_value = [
            {"name": "failing_agent", "module": __name__, "class_name": "FailingAgent", "config": {}}
        ]
        llm_manager_mock = mocker.MagicMock()
        context_manager_mock = mocker.MagicMock()
        orchestrator = AgentOrchestrator(config_manager=config_manager_mock, llm_manager=llm_manager_mock, context_manager=context_manager_mock)
        orchestrator.load_agents()
        return orchestrator

    @pytest.mark.asyncio
    async def test_orchestrator_handles_agent_failure(orchestrator, caplog):
        feature_request = "Test Feature"
        context = {}
        with pytest.raises(Exception, match="Agent failed"):
            await orchestrator.execute_agents(feature_request, context)
        assert "Agent failed" in caplog.text