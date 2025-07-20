# FEATURE: Context Accumulation in ContextManager

## EXECUTIVE SUMMARY
This feature enhances the `ContextManager` to accumulate context data over time, rather than just storing the latest state. This enables agents to access the historical evolution of any piece of data, allowing for more sophisticated analysis, summarization, and decision-making based on past events.

## CODEBASE ANALYSIS
The existing `core/context_manager.py` implements a simple key-value store using a Python dictionary. The `set()` method currently overwrites any existing value for a key, meaning all historical context is lost. The `get()` method retrieves the single, current value. This feature will require modifying the internal data structure to store a history of values for each key and introducing new methods to manage this accumulation without breaking the existing interface that other components rely on.

## DOMAIN RESEARCH
In multi-agent and orchestration systems, maintaining a complete history of operations and data transformations is crucial for debugging, auditing, and enabling more intelligent agent behavior. A common pain point is agents making decisions with incomplete information because they can only see the final state of a previous step, not the reasoning or alternatives that led to it. The industry standard pattern is to move from simple state-setting to an event-sourcing or log-based approach, where every change is recorded as an immutable event. This feature implements a simplified version of this by accumulating values in a list for each context key.

## TECHNICAL APPROACH
The recommended approach is to change the internal `_context` from `Dict[str, Any]` to `Dict[str, List[Any]]`. This allows each key to hold a chronological list of values.

1.  **New Method `add(key, value)`**: This will be the primary method for accumulation. It will append a new value to the list associated with a key.
2.  **Modify `get(key)`**: To maintain backward compatibility, `get()` will be modified to return only the *most recent* value from the list.
3.  **New Method `get_history(key)`**: This method will be added to allow agents to retrieve the entire list of historical values for a key.
4.  **Modify `set(key, value)`**: The existing `set()` method will be retained but its behavior will be to overwrite the entire history for a key with a new list containing only the new value. This provides a way to explicitly reset or override context history when needed.

An alternative would be to store timestamped values, but this adds complexity that is not required for the immediate need. The list-based approach is sufficient and less disruptive.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required. The context is managed in-memory.

### API Design
The public interface of the `ContextManager` class will be modified.

**`core/context_manager.py`**
-   `_context`: `Dict[str, List[Any]]`
-   `add(self, key: str, value: Any) -> None`: Appends `value` to the list at `self._context[key]`.
-   `get(self, key: str, default: Any = None) -> Any`: Returns the last item in the list for the given `key`, or `default` if the key doesn't exist.
-   `set(self, key: str, value: Any) -> None`: Overwrites the list at `self._context[key]` with `[value]`.
-   `get_history(self, key: str) -> List[Any]`: Returns the entire list for the given `key`, or an empty list if the key doesn't exist.
-   `update(self, data: Dict[str, Any]) -> None`: This method's behavior will be to call `set()` for each key-value pair in the input dictionary, effectively overwriting the history for each key.

### Frontend Components
N/A. This is a backend architectural change.

### Backend Services
The `ContextManager` is the primary service affected. Other services like the `AgentOrchestrator` will consume this new functionality. No other services require direct modification for this feature, but they will benefit from the new capabilities in the future.

## RISK ASSESSMENT
### Technical Risks
-   **Memory Usage**: Storing an unbounded history for every context variable could lead to high memory consumption.
    -   **Mitigation**: For this initial implementation, we will accept this risk. A follow-up feature should introduce a configurable history limit (e.g., "keep last N items") to manage memory.
-   **Breaking Changes**: Incorrectly modifying the `get` method could break existing agents that expect a single value.
    -   **Mitigation**: The technical approach is designed to maintain the `get` method's signature and return type, ensuring it still provides a single value (the latest one), which prevents breaking existing integrations.

### Business Risks
-   **Performance Degradation**: If context histories become extremely large, appending and retrieving values could introduce minor performance overhead.
    -   **Mitigation**: The use of Python lists makes append operations O(1). Retrieval of the last item is also O(1). The risk is minimal for reasonably sized histories. The memory-limiting mitigation will also address this.

## PROJECT DETAILS
**Estimated Effort**: 1 day (includes implementation and testing)
**Dependencies**: None
**Priority**: Medium
**Category**: feature

## IMPLEMENTATION DETAILS
-   **Files to create**:
    -   `tests/core/test_context_manager.py`
-   **Files to modify**:
    -   `core/context_manager.py`
-   **Key classes/functions to implement**:
    -   In `ContextManager`:
        -   Modify `__init__`, `get`, `set`, `update`.
        -   Add `add`, `get_history`.
-   **Acceptance criteria for "done"**:
    -   All existing and new methods in `ContextManager` are implemented as specified.
    -   A comprehensive suite of unit tests in `tests/core/test_context_manager.py` validates the functionality.
    -   The system runs without errors after the changes.

## SCOPE BOUNDARIES
**IN SCOPE**:
-   Implementing the list-based context accumulation logic within `ContextManager`.
-   Adding `add` and `get_history` methods.
-   Ensuring `get` and `set` work as specified for backward compatibility.
-   Creating unit tests for the `ContextManager`.

**OUT OF SCOPE**:
-   Implementing memory management or history-limiting features.
-   Refactoring any existing agents to utilize the new `get_history` method.
-   Performance benchmarking of the new implementation.

## ACCEPTANCE CRITERIA
-   [ ] `ContextManager.add(key, value)` appends the value to a list for that key.
-   [ ] `ContextManager.get(key)` returns the most recently added value for that key.
-   [ ] `ContextManager.set(key, value)` replaces the entire history for a key with a new list containing only `value`.
-   [ ] `ContextManager.get_history(key)` returns the complete list of values for that key.
-   [ ] `ContextManager.get()` and `ContextManager.get_history()` return a default value or empty list respectively if the key does not exist.
-   [ ] All new and modified methods are covered by unit tests in `tests/core/test_context_manager.py`.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add Context Accumulation to ContextManager
**Labels**: feature, core, context
**Assignee**:
**Project**: Loom Core