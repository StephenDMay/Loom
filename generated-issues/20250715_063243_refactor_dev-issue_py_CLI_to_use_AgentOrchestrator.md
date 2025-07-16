# FEATURE: Refactor dev-issue.py CLI to use AgentOrchestrator

## EXECUTIVE SUMMARY
This refactor will decouple the issue generation logic from the `dev-issue.py` command-line interface. By moving the core logic into a dedicated `IssueGeneratorAgent`, we can leverage the `AgentOrchestrator` to manage and execute the task, aligning the tool with the project's modular, agent-based architecture and making it easier to extend in the future.

## CODEBASE ANALYSIS
- **dev-issue.py**: This is a monolithic script that currently handles everything: argument parsing, configuration loading, prompt construction, LLM invocation via `subprocess`, and file output. The core logic is within the `DevIssueGenerator` class, specifically the `generate_issue` method. It directly reads a meta-prompt template and injects context to generate a final prompt for the LLM.
- **agents/orchestrator.py**: The `AgentOrchestrator` is designed to load, list, and execute agents. It discovers agents by looking for `manifest.json` files in subdirectories. It can instantiate and run an agent's `execute` method, making it the ideal component to abstract away the specific details of how an issue is generated.
- **agents/base_agent.py**: Defines the `BaseAgent` abstract class with a single `execute` method. Any new agent must inherit from this class.
- **Integration Points**: The primary integration point will be in the `main` function of `dev-issue.py`. Instead of instantiating and calling `DevIssueGenerator`, it will instantiate the `AgentOrchestrator`, request the `issue-generator` agent, and call its `execute` method, passing the feature description and any other relevant options as arguments.

## DOMAIN RESEARCH
- **User Workflow**: A developer wants to quickly generate a structured development issue from a simple command-line input (e.g., `python dev-issue.py "my feature idea"`). The process should be fast, reliable, and consistent.
- **Industry Patterns**: The proposed change aligns with the Strategy design pattern and the principle of Separation of Concerns. The CLI acts as the context, the `AgentOrchestrator` as the strategy invoker, and the `IssueGeneratorAgent` as a concrete strategy. This is a standard pattern for building extensible systems where different tasks (agents) can be added, removed, or swapped without changing the client (the CLI).
- **Competitive Analysis**: Many CLI tools (e.g., `git`, `docker`, `kubectl`) use a similar command/sub-command structure that dispatches tasks to different handlers. This refactor moves `dev-issue.py` closer to that robust and scalable model.

## TECHNICAL APPROACH
The recommended approach is to create a new, dedicated agent for issue generation and modify the CLI to use it.

1.  **Create `IssueGeneratorAgent`**:
    *   A new directory `agents/issue_generator/` will be created.
    *   It will contain an `agent.py` with an `IssueGeneratorAgent` class that inherits from `BaseAgent`.
    *   The logic from `DevIssueGenerator.generate_issue` will be moved into the `IssueGeneratorAgent.execute` method. This includes loading the config, reading the meta-prompt, building the final prompt, and invoking the LLM.
    *   A `manifest.json` file will be created to register the agent with the `AgentOrchestrator`.
2.  **Refactor `dev-issue.py`**:
    *   The `DevIssueGenerator` class will be removed.
    *   The `main` function will be simplified to:
        *   Parse command-line arguments (`--prompt`, `--dry-run`, etc.).
        *   Instantiate `AgentOrchestrator`.
        *   Call `orchestrator.execute_agent('issue-generator', task=feature_description, dry_run=args.dry_run)`.
    *   The `execute` method of the new agent will handle the rest, returning the final generated markdown. The CLI will then be responsible for saving the file and handling GitHub integration.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
The CLI's API will be simplified and standardized.

**Proposed CLI command:**
`python dev-issue.py --prompt "Your feature description" [--dry-run]`

The `--template` and `--provider` arguments will be passed as parameters to the agent's `execute` method.

### Frontend Components
N/A.

### Backend Services
- **`dev-issue.py` (CLI Client)**:
    - Becomes a lightweight client for the `AgentOrchestrator`.
    - Primary responsibility is parsing user input and dispatching to the orchestrator.
- **`agents/issue_generator/agent.py` (New Service)**:
    - Contains the `IssueGeneratorAgent` class.
    - The `execute` method will encapsulate all the business logic for generating an issue.
    - It will accept parameters like `prompt`, `template_type`, `provider`, and `dry_run`.
- **`AgentOrchestrator` (Existing Service)**:
    - No changes are needed. It will automatically discover and load the new agent.

## RISK ASSESSMENT
### Technical Risks
- **Incomplete Orchestrator Features**: The `AgentOrchestrator` might not currently support passing complex arguments (like `dry_run`) to agents gracefully.
    - **Mitigation**: The orchestrator's `execute_agent` method will be updated to accept `*args` and `**kwargs` and pass them directly to the agent's `execute` method, making it fully flexible.
- **Output Inconsistency**: The refactored logic might produce slightly different markdown output than the original script.
    - **Mitigation**: Run the old and new versions in parallel on the same input and `diff` the results to ensure they are identical before finalizing the change.

### Business Risks
- **Refactoring Effort**: The refactor might take longer than expected if unforeseen complexities arise in the interaction between the CLI and the agent.
    - **Mitigation**: The scope is well-defined. The `DevIssueGenerator` class provides a clear blueprint for the agent's logic, minimizing discovery time.

## PROJECT DETAILS
**Estimated Effort**: 0.5 days
**Dependencies**: A functional `AgentOrchestrator` class.
**Priority**: High
**Category**: technical-debt

## IMPLEMENTATION DETAILS
- **Files to Create**:
    - `agents/issue_generator/agent.py`
    - `agents/issue_generator/manifest.json`
- **Files to Modify**:
    - `dev-issue.py` (major refactor, removing `DevIssueGenerator` class)
    - `agents/orchestrator.py` (minor change to `execute_agent` to support `**kwargs`)
- **Key Classes/Functions to Implement**:
    - `class IssueGeneratorAgent(BaseAgent)`
    - `def execute(self, prompt: str, **kwargs)`
- **CLI Command Structure**:
    - `python dev-issue.py --prompt "Implement user auth"`
- **Acceptance Criteria**:
    - The command `python dev-issue.py --prompt "test"` successfully generates an issue file in `generated-issues/`.
    - The generated file's content and format are identical to the output of the original script.
    - The `--dry-run` flag works as expected, printing the prompt without calling the LLM.

## SCOPE BOUNDARIES
- **IN SCOPE**:
    - Creating the `IssueGeneratorAgent`.
    - Refactoring `dev-issue.py` to use the orchestrator.
    - Ensuring existing functionality (`--dry-run`, file output, etc.) works correctly through the new architecture.
- **OUT OF SCOPE**:
    - Adding new features to the issue generation process.
    - Changing the `meta-prompt-template.md`.
    - Refactoring any other part of the system.

## ACCEPTANCE CRITERIA
- [ ] `dev-issue.py` no longer contains the `DevIssueGenerator` class.
- [ ] A new agent exists at `agents/issue_generator/` and is loaded by `AgentOrchestrator`.
- [ ] Running `python dev-issue.py --prompt "test feature"` executes the `IssueGeneratorAgent` via the orchestrator.
- [ ] The generated markdown file is functionally identical to one generated by the previous version of the script.
- [ ] The `--dry-run` option is functional and prints the prompt that would be sent to the LLM.

## GITHUB ISSUE TEMPLATE
**Title**: Refactor: Use AgentOrchestrator in dev-issue.py
**Labels**: `refactor`, `technical-debt`, `architecture`
**Assignee**:
**Project**: Core Infrastructure
