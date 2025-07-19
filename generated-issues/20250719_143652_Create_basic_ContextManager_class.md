# FEATURE: Create basic ContextManager class

## EXECUTIVE SUMMARY
This feature introduces a foundational `ContextManager` class responsible for tracking and managing the state of conversations and operations. This enables the system to maintain context across multiple interactions, allowing for more complex, multi-step tasks and coherent AI-driven workflows.

## CODEBASE ANALYSIS
The current system lacks a formal context management mechanism. The `AgentOrchestrator` loads and runs agents, and the `LLMManager` handles interactions with language models, but there is no standardized way to pass conversational history or state between agent executions or LLM calls. Each transaction is largely stateless.

- **Integration Points**:
    - `core/llm_manager.py`: The `LLMManager` will need to be modified to accept a context object from the `ContextManager` and pass it to the underlying model APIs. This is the primary consumer of the context.
    - `agents/orchestrator.py`: The `AgentOrchestrator` will likely be responsible for instantiating and managing the lifecycle of the `ContextManager`, ensuring that context is maintained across an entire session or task.
    - `agents/base_agent.py`: The `execute` method of the `BaseAgent` may need to be updated to receive and update the context, allowing agents to be aware of the conversational history.

- **Required Architectural Changes**:
    - A new core component (`core/context_manager.py`) will be introduced.
    - Existing method signatures in the `LLMManager` and `AgentOrchestrator` will need to be updated to handle the new context object.

## DOMAIN RESEARCH
In conversational AI and agent-based systems, context is critical. Users expect the system to remember previous turns of a conversation and prior actions.

- **User Workflows**: A developer using this system will perform a series of steps to accomplish a goal (e.g., "analyze this file", "now write tests for it", "now refactor the tested code"). Each step depends on the context of the previous ones.
- **Industry Patterns**:
    1.  **Rolling History Window**: The most common pattern for chatbots is to maintain a list of the last N messages or tokens. This is simple and effective for short-to-medium conversations.
    2.  **Summarization**: For very long conversations, a separate LLM call is used to summarize the history to keep the context window from overflowing.
    3.  **Vector Stores (RAG)**: For knowledge-intensive tasks, context is augmented by retrieving relevant information from a vector database.
- **Competitive Solutions**: Most AI development platforms (e.g., LangChain, LlamaIndex) have robust context/memory management as a central feature. This feature is a foundational step towards that level of capability.

## TECHNICAL APPROACH
The recommended approach is to create a simple, in-memory `ContextManager` class. This provides the core functionality with minimal complexity, allowing for future expansion.

- **Primary Approach**:
    1.  Create a `ContextManager` class in a new file: `core/context_manager.py`.
    2.  The class will internally store a list of messages, where each message is a dictionary (e.g., `{'role': 'user', 'content': '...'}`).
    3.  It will expose methods like `add_message(role, content)`, `get_context()`, and `clear()`.
    4.  The `AgentOrchestrator` will create an instance of `ContextManager` and pass it to agents during execution.
    5.  The `LLMManager` will be updated to accept this context and format it for the specific model API being called.

- **Alternative Approaches**:
    - **Persistent Context**: Storing context to disk (e.g., in a JSON file or a SQLite database). This is more complex and should be a separate feature for session persistence.
    - **Advanced Context**: Implementing summarization or RAG. This is out of scope for a "basic" context manager.

## IMPLEMENTATION SPECIFICATION
### Database Changes
- None. This implementation will be in-memory.

### API Design
This is an internal class, so no public-facing API changes are needed. The class interface will be:
- `class ContextManager:`
    - `__init__(self, max_history_size=50)`
    - `add_message(self, role: str, content: str)`
    - `get_context(self) -> list[dict]`
    - `clear(self)`

### Frontend Components
- N/A. This is a backend feature.

### Backend Services
- **`core/context_manager.py`**:
    - New file containing the `ContextManager` class.
    - The class will manage a `deque` (double-ended queue) to efficiently enforce the `max_history_size`.
- **`core/llm_manager.py`**:
    - The `execute_llm` method (or equivalent) will be modified from `execute_llm(self, prompt)` to `execute_llm(self, context: list[dict], prompt: str)`.
    - It will be responsible for combining the existing context with the new prompt before sending it to the model.
- **`agents/orchestrator.py`**:
    - The main execution loop will instantiate `ContextManager`.
    - It will pass the context manager instance to each agent it runs.

## RISK ASSESSMENT
### Technical Risks
- **Unbounded Memory Growth**: If not capped, the context history could consume significant memory.
    - **Mitigation**: Implement a `max_history_size` in the constructor to limit the number of messages stored.
- **API Incompatibility**: Modifying method signatures in core classes (`LLMManager`, `AgentOrchestrator`) is a breaking change for existing agents.
    - **Mitigation**: This is early-stage development, so breaking changes are acceptable. Communicate the change clearly.

### Business Risks
- **Poor Context Handling**: If the context is not managed correctly, it can lead to nonsensical or incorrect AI responses, frustrating the user.
    - **Mitigation**: Start with a simple, well-understood rolling history window and write clear unit tests.

## PROJECT DETAILS
**Estimated Effort**: 1-2 days
**Dependencies**: None. This is a foundational component.
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to Create**:
    - `core/context_manager.py`
    - `tests/core/test_context_manager.py`
- **Files to Modify**:
    - `core/llm_manager.py`
    - `agents/orchestrator.py`
    - `agents/base_agent.py` (potentially the `execute` method signature)
- **Key Classes/Functions**:
    - `class ContextManager`
    - `LLMManager.execute_llm(...)`
    - `AgentOrchestrator.run_agents(...)`
- **Acceptance Criteria**:
    - A test can demonstrate that after one agent runs, the context it generated is available to a subsequent agent.
    - The `LLMManager` correctly prepends the context to the prompt before making an API call.

## SCOPE BOUNDARIES
**IN SCOPE**:
- An in-memory `ContextManager` class that stores a list of messages.
- A configurable limit to the number of messages stored.
- Integration with `LLMManager` and `AgentOrchestrator`.

**OUT OF SCOPE**:
- Persisting context to disk or a database.
- Context summarization techniques.
- Retrieval-Augmented Generation (RAG) or vector stores.
- Thread-safety or multi-user context management.

## ACCEPTANCE CRITERIA
- [ ] `core/context_manager.py` is created with the `ContextManager` class.
- [ ] `ContextManager` has methods to add a message and retrieve the current context.
- [ ] `ContextManager` respects a maximum history size.
- [ ] `LLMManager` is modified to accept and use the context.
- [ ] `AgentOrchestrator` instantiates and passes the `ContextManager` to agents.
- [ ] Unit tests for `ContextManager` are created and pass.
- [ ] An integration test demonstrates context is passed between two agent executions.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Create basic ContextManager class
**Labels**: feature, core, architecture
**Assignee**:
**Project**: Core System