# FEATURE: Create minimal PromptAssemblyAgent template

## EXECUTIVE SUMMARY
This feature introduces a new agent, the `PromptAssemblyAgent`, responsible for dynamically constructing prompts for other agents from templates and context. This will centralize prompt logic, improve maintainability, and enable more sophisticated, context-aware prompt generation.

## CODEBASE ANALYSIS
The `PromptAssemblyAgent` will be a new agent, similar in structure to the existing `ProjectAnalysisAgent`. It will inherit from `BaseAgent` and be managed by the `Orchestrator`. It will not directly modify existing code but will be used by other agents to assemble prompts. It will read template files and utilize the `ContextManager` to get data for populating those templates.

Key integration points:
- `agents/base_agent.py`: To be subclassed.
- `core/context_manager.py`: To read context data.
- `agents/orchestrator.py`: To be called by the orchestrator.

No significant technical debt will be incurred. This is a foundational component for a more robust agent system.

## DOMAIN RESEARCH
In multi-agent systems, managing prompts is a common challenge. Centralizing prompt generation is a best practice. It allows for easier A/B testing of prompts, versioning, and adaptation to different LLM providers. Users (developers) will benefit from more consistent and powerful agent behavior without having to manage prompt strings scattered throughout the codebase.

## TECHNICAL APPROACH
The recommended approach is to create a new directory `agents/prompt_assembly_agent` containing `agent.py`, `config.json`, and `manifest.json`. The `agent.py` will contain the `PromptAssemblyAgent` class, which will have an `execute` method that takes a template name and a context dictionary as input. It will load the specified template, fill it with the provided context, and return the assembled prompt.

An alternative would be to make this a utility function within the `llm_manager`, but creating a dedicated agent is more aligned with the project's multi-agent architecture and allows for more complex prompt logic in the future.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
A new `PromptAssemblyAgent` will be created. Its `execute` method will have the signature: `execute(self, template_name: str, context: Dict) -> str`.

## RISK ASSESSMENT
### Technical Risks
- **Template Not Found**: The agent must handle cases where a template file is missing.
  - **Mitigation**: Implement robust error handling and logging.
- **Incomplete Context**: The context provided might be missing required keys for the template.
  - **Mitigation**: The agent should allow for missing keys, leaving placeholders in place or using default values.

### Business Risks
- **Performance**: If prompt assembly is slow, it could impact the overall performance of the system.
  - **Mitigation**: The initial implementation will be simple string replacement, which is fast. Caching could be added later if needed.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to create**:
    - `agents/prompt_assembly_agent/agent.py`
    - `agents/prompt_assembly_agent/config.json`
    - `agents/prompt_assembly_agent/manifest.json`
- **Key classes/functions to implement**:
    - `agents.prompt_assembly_agent.agent.PromptAssemblyAgent`
        - `execute(self, template_name: str, context: Dict) -> str`
- **Exact CLI command structure**: N/A (This is a library-level component)
- **Clear acceptance criteria for "done"**:
    - The `PromptAssemblyAgent` can be instantiated.
    - The `execute` method returns a string with placeholders from a template file replaced with values from a context dictionary.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Creating the `PromptAssemblyAgent` with basic template loading and placeholder replacement.
- Creating the necessary config and manifest files.

**OUT OF SCOPE**:
- Integrating the `PromptAssemblyAgent` with other agents.
- Advanced templating logic (e.g., loops, conditionals).
- Caching of templates or assembled prompts.

## ACCEPTANCE CRITERIA
- [ ] `PromptAssemblyAgent` class is created in `agents/prompt_assembly_agent/agent.py`.
- [ ] `PromptAssemblyAgent` inherits from `BaseAgent`.
- [ ] `execute` method takes `template_name` and `context` as arguments.
- [ ] `execute` method loads a template file from a `templates` directory.
- [ ] `execute` method replaces placeholders in the format `{{ placeholder }}` with values from the context.
- [ ] `config.json` and `manifest.json` are created for the agent.

## GITHUB ISSUE TEMPLATE
**Title**: Create minimal PromptAssemblyAgent template
**Labels**: feature, agent
**Assignee**:
**Project**: Loom