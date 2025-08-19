# FEATURE: PromptAssemblyAgent

## EXECUTIVE SUMMARY
The PromptAssemblyAgent is a core component responsible for dynamically constructing prompts for other agents. It will combine templates, context, and user input to generate a final, executable prompt, ensuring consistency and flexibility in how the system interacts with LLMs.

## CODEBASE ANALYSIS
The `PromptAssemblyAgent` will be a new agent, similar in structure to the `FeatureResearchAgent`. It will inherit from `BaseAgent` and be managed by the `AgentOrchestrator`. It will need a manifest.json and a config.json. It will primarily interact with the `ContextManager` to retrieve context and will not directly call the `LLMManager`. Its output will be a string (the assembled prompt) that other agents will then use.

## DOMAIN RESEARCH
In AI-driven development automation, prompt engineering is critical. A dedicated agent for prompt assembly allows for:
-   **Consistency:** Standardized prompt structures across the system.
-   **Maintainability:** Centralized management of prompt templates.
-   **Flexibility:** Easy adaptation to different LLM providers and models with varying prompt format requirements.
-   **Experimentation:** A/B testing of different prompt strategies.

## TECHNICAL APPROACH
The recommended approach is to create a `PromptAssemblyAgent` that takes a template name, a dictionary of placeholders, and a list of context keys as input. It will load the specified template, retrieve the requested context from the `ContextManager`, and then replace the placeholders in the template with the provided values and context.

An alternative approach would be to have a more "intelligent" agent that uses an LLM to help assemble the prompt. This is more complex and not necessary for the initial implementation.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
A new `PromptAssemblyAgent` class will be created in `agents/prompt_assembly_agent/agent.py`.

## RISK ASSESSMENT
### Technical Risks
-   **Template Not Found:** The agent must handle cases where the specified template does not exist. Mitigation: Clear error messages and logging.
-   **Missing Context:** The agent should gracefully handle missing context keys. Mitigation: Allow for optional context keys and default values.

### Business Risks
-   **Poorly Designed Prompts:** If the assembled prompts are not effective, the performance of downstream agents will suffer. Mitigation: Extensive testing and iteration on prompt templates.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
-   Create `agents/prompt_assembly_agent/agent.py`
-   Create `agents/prompt_assembly_agent/manifest.json`
-   Create `agents.prompt_assembly_agent/config.json`
-   The `execute` method will take `template_name`, `placeholders`, and `context_keys` as arguments.
-   The agent will need a mechanism to load templates from a `templates` directory.

## SCOPE BOUNDARIES
**IN SCOPE:**
-   Loading prompt templates from files.
-   Replacing placeholders in templates.
-   Injecting context from the `ContextManager`.
-   Returning the assembled prompt as a string.

**OUT OF SCOPE:**
-   Using an LLM to generate or modify prompts.
-   Managing the lifecycle of prompt templates (this will be done manually for now).

## ACCEPTANCE CRITERIA
-   [ ] The `PromptAssemblyAgent` can be loaded by the `AgentOrchestrator`.
-   [ ] The agent can load a specified prompt template.
-   [ ] The agent can replace placeholders in the template with provided values.
-   [ ] The agent can inject context from the `ContextManager` into the template.
-   [ ] The agent returns the fully assembled prompt as a string.

## GITHUB ISSUE TEMPLATE
**Title**: Create PromptAssemblyAgent for dynamic prompt construction
**Labels**: feature, agent
**Assignee**:
**Project**: Loom