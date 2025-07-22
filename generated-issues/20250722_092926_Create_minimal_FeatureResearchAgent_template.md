# FEATURE: Create minimal FeatureResearchAgent template

## EXECUTIVE SUMMARY
This feature introduces a new agent template, the `FeatureResearchAgent`, designed to standardize and eventually automate the process of feature research and specification. By creating a minimal, well-defined structure for this agent, we enable consistent, high-quality planning documents and pave the way for future AI-driven analysis of feature requests.

## CODEBASE ANALYSIS
The current codebase has a clear pattern for agents located in the `agents/` directory. Each agent (e.g., `project_analysis_agent`, `issue_generator`) consists of a directory containing:
- `agent.py`: The core logic, inheriting from `agents.base_agent.BaseAgent`.
- `manifest.json`: Metadata describing the agent's purpose, name, and entry point.
- `config.json`: Agent-specific settings, such as model parameters or file paths.
- `templates/`: A directory for prompt or output templates.

The new `FeatureResearchAgent` will follow this existing architectural pattern. It will be a new directory `agents/feature_research_agent/` containing the standard set of files. It will be invoked by the `Orchestrator` and will not require any changes to the core system (`core/`) for this minimal implementation. The primary integration point is adhering to the `BaseAgent` interface.

## DOMAIN RESEARCH
The user's core workflow is to take a feature idea and produce a comprehensive technical plan. The provided meta-prompt *is* the domain research, defining a robust process for feature analysis that covers technical, business, and project management aspects.

This process is currently manual. Automating it, even partially, will reduce cognitive load on developers, enforce best practices for planning, and ensure all critical aspects (security, testing, risks) are considered upfront. The minimal template serves as the first step, creating a "fill-in-the-blanks" document that structures the research process.

## TECHNICAL APPROACH
The recommended approach is to create the scaffolding for the new agent without implementing the full AI-driven analysis logic initially.

1.  **Create Directory Structure**: Add a new directory: `agents/feature_research_agent/`.
2.  **Add Agent Manifest**: Create `agents/feature_research_agent/manifest.json` to make the agent discoverable by the system.
3.  **Add Agent Configuration**: Create `agents/feature_research_agent/config.json` with placeholder values for model configuration.
4.  **Create Agent Template**: Copy the user-provided `meta-prompt-template.md` to `agents/feature_research_agent/templates/feature_research_template.md`. This will be the core template the agent uses.
5.  **Create Agent Class**: Create `agents/feature_research_agent/agent.py` with a `FeatureResearchAgent` class that inherits from `BaseAgent`. The initial `run` method will be a placeholder, simply loading the template and replacing a variable with the feature name.

An alternative would be to create a single script, but that would deviate from the established agent-based architecture and limit future extensibility.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None. The agent operates internally.

### Frontend Components
None.

### Backend Services
A new `FeatureResearchAgent` class will be created in `agents/feature_research_agent/agent.py`. It will have a `run(feature_description: str)` method that:
1.  Loads the template from `templates/feature_research_template.md`.
2.  Replaces a placeholder (e.g., `[FEATURE_TO_ANALYZE]`) in the template with the `feature_description`.
3.  Returns the populated template as a string.

## RISK ASSESSMENT
### Technical Risks
- **Risk 1**: Deviation from the existing agent pattern.
  - **Mitigation**: Closely model the new agent's structure on the existing `project_analysis_agent`.

### Business Risks
- **Risk 1**: The template is too rigid and discourages creative planning.
  - **Mitigation**: The initial template is comprehensive but can be iterated upon based on team feedback. It's a starting point, not a final, unchangeable document.

## PROJECT DETAILS
**Estimated Effort**: 0.5 days
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to create**:
    - `agents/feature_research_agent/manifest.json`
    - `agents/feature_research_agent/config.json`
    - `agents/feature_research_agent/agent.py`
    - `agents/feature_research_agent/templates/feature_research_template.md`
- **Key classes/functions to implement**:
    - `class FeatureResearchAgent(BaseAgent)` in `agent.py`.
    - `def run(self, feature_description: str)` method within the class.
- **CLI command structure**:
    - The agent would be invoked via the orchestrator, not directly. e.g., `python loom.py --agent feature_research_agent --request "New feature idea"`
- **Acceptance criteria for "done"**:
    - The agent files and directory structure are created as specified.
    - The agent can be successfully listed and invoked by the orchestrator.
    - When invoked, the agent correctly populates the feature name in the template and returns the result without errors.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Creating the directory structure and all necessary files (`agent.py`, `config.json`, `manifest.json`, template file) for the new agent.
- Implementing a minimal `run` method that loads the template and replaces the feature name.

**OUT OF SCOPE**:
- Implementing any LLM-based logic to automatically fill out the research template.
- Generating output files; the agent will return the populated markdown as a string for now.
- Any UI for interacting with the agent.

## ACCEPTANCE CRITERIA
- [ ] The directory `agents/feature_research_agent/` exists.
- [ ] The agent contains `agent.py`, `config.json`, `manifest.json`, and `templates/feature_research_template.md`.
- [ ] The `FeatureResearchAgent` class in `agent.py` inherits from `BaseAgent`.
- [ ] Invoking the agent via the orchestrator with a feature description returns the content of the template with the feature name correctly inserted.

## GITHUB ISSUE TEMPLATE
**Title**: feat: Create minimal FeatureResearchAgent template
**Labels**: feature, agent, planning
**Assignee**:
**Project**: Loom Development