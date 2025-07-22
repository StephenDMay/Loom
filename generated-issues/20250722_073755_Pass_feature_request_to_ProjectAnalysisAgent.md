# FEATURE: Pass feature request to ProjectAnalysisAgent

## EXECUTIVE SUMMARY
This feature enables the `ProjectAnalysisAgent` to receive and utilize a specific feature request, focusing its analysis on the areas of the codebase relevant to the requested changes. This will provide more targeted and useful context for downstream agents in the development pipeline.

## CODEBASE ANALYSIS
The current implementation starts in `loom.py`, where a feature description is passed to the `AgentOrchestrator`. The orchestrator's `run_sequence` method takes this description as `initial_task`. However, the `ProjectAnalysisAgent`'s `execute` method currently defaults to a generic "General project analysis" and doesn't effectively use the incoming task. The `execute` method signature in `BaseAgent` is `(*args, **kwargs)`, which is flexible enough to handle this. The integration point will be modifying the `ProjectAnalysisAgent` to correctly handle the `initial_task` passed by the orchestrator.

## DOMAIN RESEARCH
For an automated development system, understanding the specific feature request is paramount. A generic analysis of the entire project is inefficient and provides low-quality context. Industry best practices for code generation and modification tasks emphasize providing the AI with a narrow, relevant context. This feature aligns with that principle by using the feature request to guide the analysis, making the entire process more efficient and the results more accurate.

## TECHNICAL APPROACH
The recommended approach is to modify the `ProjectAnalysisAgent.execute` method to directly use the first positional argument as the feature request. This aligns with how the `AgentOrchestrator` is designed to work, passing the output of one agent as the input to the next.

The `execute` method in `ProjectAnalysisAgent` will be changed from:
`def execute(self, *args, **kwargs) -> str:`
to a more explicit signature that expects the feature request.

The `feature_request` in the `template_context` will be populated from this argument.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
- **`agents/orchestrator.py`**: No changes are immediately necessary, as it already passes the `initial_task` to the first agent.
- **`agents/project_analysis_agent/agent.py`**: The `execute` method will be updated to properly receive and process the feature request.

## RISK ASSESSMENT
### Technical Risks
- **Incorrect Argument Handling**: The agent might not correctly interpret the arguments passed by the orchestrator.
  - **Mitigation**: Add a unit test to ensure the feature request is correctly passed and used.

### Business Risks
- **Analysis Quality**: If the feature request is too vague, the analysis might still be too broad.
  - **Mitigation**: This is an inherent limitation of the input quality. Future work could involve an agent that refines the user's request.

## PROJECT DETAILS
**Estimated Effort**: 1-2 hours
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to modify**: `agents/project_analysis_agent/agent.py`, `tests/integration/test_project_analysis_agent.py`
- **Key classes/functions to implement**:
    - Modify `ProjectAnalysisAgent.execute` to accept the feature request as a primary argument.
    - Update the `template_context` dictionary to use this argument.
- **CLI command structure**: No change. `python loom.py "your feature request"`
- **Acceptance criteria**:
    - When `loom.py` is run with a feature request, the `ProjectAnalysisAgent` should use that request in its analysis prompt.
    - The analysis summary stored in the `ContextManager` should reflect the focus of the feature request.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Modifying `ProjectAnalysisAgent` to accept and use a feature request string.
- Ensuring the feature request is passed through the `AgentOrchestrator`.
- Updating tests to validate this functionality.

**OUT OF SCOPE**:
- Any validation or clarification of the feature request itself.
- Changing how other agents consume the analysis.

## ACCEPTANCE CRITERIA
- [ ] The `ProjectAnalysisAgent.execute` method signature is updated to explicitly handle a feature request string.
- [ ] The feature request is used to populate the `feature_request` placeholder in the analysis template.
- [ ] An integration test verifies that a feature request provided via the CLI is used by the `ProjectAnalysisAgent`.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Pass feature request to ProjectAnalysisAgent
**Labels**: enhancement, agent-framework
**Assignee**:
**Project**: Loom Phase 1