# FEATURE: Test Agent Configuration System

## EXECUTIVE SUMMARY
This feature introduces a standardized testing framework for agent configurations. It will allow developers to validate their agent's `config.json` and `manifest.json` files, ensuring they are correctly structured and can be successfully loaded by the `AgentOrchestrator`, thereby reducing runtime errors and improving developer experience.

## CODEBASE ANALYSIS
The current system uses a `core/config_manager.py` to handle configuration loading and an `agents/orchestrator.py` to load and manage agents. Each agent (e.g., `agents/example_agent/`) contains its own `config.json` and `manifest.json`. While the `ConfigManager` resolves and provides these configurations at runtime, there is no dedicated, isolated mechanism for developers to test their agent's configuration before it's integrated and run by the orchestrator. This feature will primarily integrate with the existing `pytest` infrastructure in the `tests/` directory.

## DOMAIN RESEARCH
A key developer workflow is creating a new agent. A common pain point in modular systems like this is debugging configuration errors that only appear at runtime. Industry best practice is to provide tools for "shift-left" testing, allowing developers to catch errors early. By providing a simple, repeatable way to test an agent's configuration files, we can significantly reduce integration friction and improve the robustness of the agent ecosystem. This is a foundational feature for ensuring the platform remains stable as more agents are developed.

## TECHNICAL APPROACH
The recommended approach is to create a set of `pytest` helper functions or fixtures. These utilities will encapsulate the logic for finding, loading, and validating an agent's configuration files, mirroring the process used by the `AgentOrchestrator` and `ConfigManager`. This approach is preferable to a standalone script as it integrates seamlessly into the existing testing framework (`pytest`), allowing developers to write configuration tests alongside their functional tests for a given agent.

An alternative would be to create a new CLI command like `loom validate-agent <agent_name>`, but this adds CLI surface area and is less flexible than a `pytest`-based solution for test automation and CI pipelines.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None. This feature does not impact the database schema.

### API Design
No public-facing API changes are required. The implementation will involve adding new internal helper functions for testing purposes, likely within the `tests/` directory.

### Frontend Components
N/A. This is a backend development tool feature.

### Backend Services
The core logic will reside in a new test utility module. This module will leverage `core/config_manager.py` and potentially parts of `agents/orchestrator.py` to load and validate configurations in a controlled test environment. No changes to the core services themselves are anticipated; we will be using them as libraries.

## RISK ASSESSMENT
### Technical Risks
- **Tight Coupling with ConfigManager**: The test utilities might become too tightly coupled to the implementation details of `ConfigManager`.
  - **Mitigation**: The test helpers should use the public methods of `ConfigManager` as much as possible, treating it like a black box to reduce coupling.
- **Incomplete Validation**: The initial validation logic may not cover all possible configuration errors.
  - **Mitigation**: The validation system should be designed to be extensible, allowing new validation rules to be added over time as the configuration schema evolves.

### Business Risks  
- **Low Adoption**: Developers might not use the new testing utilities.
  - **Mitigation**: Document the feature clearly and update the `example_agent` to include a configuration test, setting a clear precedent.

## PROJECT DETAILS
**Estimated Effort**: 2 days
**Dependencies**: None. This is a foundational feature.
**Priority**: High
**Category**: technical-debt

## IMPLEMENTATION DETAILS
- **Files to Create**:
  - `tests/core/test_agent_configs.py`: A new test file to house the tests for agent configurations.
  - `tests/helpers.py`: A new file for shared test utilities, if one doesn't exist.
- **Key Functions to Implement**:
  - `load_and_validate_agent_config(agent_name: str) -> dict`: A helper function in `tests/helpers.py` that:
    1. Locates the agent's directory.
    2. Reads and parses `manifest.json`.
    3. Reads and parses `config.json`.
    4. Uses `ConfigManager` to get the fully resolved agent configuration.
    5. Performs basic assertions (e.g., required keys from the manifest are present).
  - `test_example_agent_config()`: A test function in `tests/core/test_agent_configs.py` that uses the helper to validate the `example_agent`.
- **CLI Command Structure**: N/A. The feature will be exposed via `pytest`.
- **Acceptance Criteria**:
  - Running `pytest tests/core/test_agent_configs.py` should pass for the valid `example_agent`.
  - If `agents/example_agent/config.json` is temporarily corrupted (e.g., made invalid JSON), the test must fail with a clear error.
  - If a key defined as required in the manifest is removed from the config, the test must fail.

## SCOPE BOUNDARIES
**IN SCOPE**:
- A `pytest`-based utility for validating the structure and content of an agent's `manifest.json` and `config.json`.
- Testing the integration of the agent's configuration with the `ConfigManager`.
- An example test for the `example_agent`.

**OUT OF SCOPE**:
- Testing the *functional behavior* of an agent based on its configuration. This belongs in agent-specific functional tests.
- A UI for managing or testing configurations.
- Real-time validation in a running application.

## ACCEPTANCE CRITERIA
- [ ] A developer can import and use a test utility to validate any given agent's configuration.
- [ ] A test exists that successfully validates the default `example_agent` configuration.
- [ ] The configuration test for an agent fails if its `config.json` file is syntactically incorrect.
- [ ] The configuration test for an agent fails if its `manifest.json` file is missing or malformed.
- [ ] Documentation is updated to explain how to write a configuration test for a new agent.

## GITHUB ISSUE TEMPLATE
**Title**: Feat: Implement Agent Configuration Testing Framework
**Labels**: `enhancement`, `testing`, `technical-debt`
**Assignee**:
**Project**: Loom Development
