# FEATURE: Context-Aware Research Agent Template

## EXECUTIVE SUMMARY
This feature will enhance the `FeatureResearchAgent` by introducing a new, more structured template that aligns with our "smart context" architecture. This will enable the agent to leverage a wider range of contextual information, leading to more accurate and relevant feature research.

## CODEBASE ANALYSIS
The existing `FeatureResearchAgent` in `agents/feature_research_agent/agent.py` already has a mechanism for loading templates and discovering context from the `ContextManager`. The current context discovery is basic and relies on a hardcoded list of keys. The template itself is also simple.

The `ContextManager` in `core/context_manager.py` is flexible enough to support the new context structure without any changes.

The main changes will be to:
1.  Create a new, more detailed template file.
2.  Update the `FeatureResearchAgent` to use this new template.
3.  Enhance the context discovery mechanism in the `FeatureResearchAgent` to be more dynamic and less reliant on hardcoded keys.

## DOMAIN RESEARCH
In the domain of automated software development, the ability to understand and utilize context is paramount. Developers rely on a vast amount of information when planning and implementing features, including:

*   **Project Goals and Vision:** What is the overall objective of the project?
*   **Existing Architecture:** How is the system currently built?
*   **Codebase Patterns:** What are the established coding conventions?
*   **Technical Debt:** What are the known issues and areas for improvement?

By creating a research template that is aware of this context, we can generate feature specifications that are not only technically sound but also aligned with the project's goals and constraints.

## TECHNICAL APPROACH
The recommended approach is to:

1.  **Create a new template file** named `feature_research_template.md` in the `agents/feature_research_agent/templates/` directory. This template will be based on the "Universal Development Feature Research Meta-Prompt" provided in the problem statement.
2.  **Update the `FeatureResearchAgent`** to use this new template. This will involve changing the `template_path` in the agent's configuration.
3.  **Enhance the `_discover_available_context` method** in the `FeatureResearchAgent` to be more dynamic. Instead of a hardcoded list of keys, it should iterate through all the keys in the `ContextManager` and format them for display in the template.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
**`agents/feature_research_agent/agent.py`**
*   Modify the `__init__` method to use the new template by default.
*   Update the `_discover_available_context` method to dynamically discover all available context.
*   Update the `_render_template` method to handle the new template structure.

**`agents/feature_research_agent/templates/feature_research_template.md`**
*   Create this new file with the content of the "Universal Development Feature Research Meta-Prompt".

## RISK ASSESSMENT
### Technical Risks
*   **Template Rendering Complexity:** The new template is more complex and may require a more sophisticated rendering logic.
    *   **Mitigation:** We will use a simple string replacement for now, which should be sufficient for the initial implementation.

### Business Risks
*   **Reduced Performance:** A more complex template and context discovery mechanism could slow down the feature research process.
    *   **Mitigation:** The performance impact is expected to be minimal and can be optimized later if necessary.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
*   **Files to create/modify**:
    *   `agents/feature_research_agent/templates/feature_research_template.md` (create)
    *   `agents/feature_research_agent/agent.py` (modify)
*   **Key classes/functions to implement**:
    *   `FeatureResearchAgent._discover_available_context`
    *   `FeatureResearchAgent._render_template`
*   **Clear acceptance criteria for "done"**:
    *   The `FeatureResearchAgent` uses the new template.
    *   The agent can dynamically discover and render all available context in the template.
    *   The existing tests in `test_context_aware_feature_research.py` pass with the new implementation.

## SCOPE BOUNDARIES
**IN SCOPE:**
*   Creating the new template.
*   Updating the `FeatureResearchAgent` to use the new template.
*   Enhancing the context discovery mechanism.

**OUT OF SCOPE:**
*   Implementing a more advanced template rendering engine (e.g., Jinja2).
*   Adding new context sources to the `ContextManager`.

## ACCEPTANCE CRITERIA
*   [ ] The `FeatureResearchAgent` successfully loads and uses the `feature_research_template.md` template.
*   [ ] The `_discover_available_context` method in `FeatureResearchAgent` dynamically discovers all context from the `ContextManager`.
*   [ ] The final output of the `FeatureResearchAgent` contains the rendered template with all the available context.
*   [ ] All existing tests pass.

## GITHUB ISSUE TEMPLATE
**Title**: Implement Context-Aware Research Agent Template
**Labels**: feature, agent, research
**Assignee**:
**Project**: Loom

I will now proceed with the implementation. First, I will create the new template file.