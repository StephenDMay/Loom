# FEATURE: [Feature Name]

## EXECUTIVE SUMMARY
[2-3 sentence summary of what this feature does and why it matters]

## CODEBASE ANALYSIS
[Analysis of existing code and integration points]

## DOMAIN RESEARCH
[User workflows, industry patterns, competitive analysis]

## TECHNICAL APPROACH
[Recommended implementation strategy with alternatives]

## IMPLEMENTATION SPECIFICATION
### Database Changes
[Schema modifications, migrations needed]

### API Design
[New endpoints, modifications to existing APIs]

### Frontend Components
[UI components, state management, user interactions]

### Backend Services
[Business logic, data processing, external integrations]

## RISK ASSESSMENT
### Technical Risks
- [Risk 1]: [Description] - [Mitigation]
- [Risk 2]: [Description] - [Mitigation]

### Business Risks  
- [Risk 1]: [Description] - [Mitigation]
- [Risk 2]: [Description] - [Mitigation]

## PROJECT DETAILS
**Estimated Effort**: [X days/weeks]
**Dependencies**: [List of blocking work]
**Priority**: [High/Medium/Low] 
**Category**: [feature/enhancement/bugfix/technical-debt]

## IMPLEMENTATION DETAILS
- Specific files to create/modify
- Key classes/functions to implement  
- Exact CLI command structure
- Clear acceptance criteria for "done"

## SCOPE BOUNDARIES
What is explicitly IN scope for this feature?
What is explicitly OUT of scope and should be separate features?

## ACCEPTANCE CRITERIA
- [ ] [Testable requirement 1]
- [ ] [Testable requirement 2]  
- [ ] [Testable requirement 3]

## GITHUB ISSUE TEMPLATE
**Title**: [Feature Name]
**Labels**: [suggested labels]
**Assignee**: [if known]
**Project**: [suggested project board]
# FEATURE: Add basic template loading to ProjectAnalysisAgent

## EXECUTIVE SUMMARY
This feature enables the `ProjectAnalysisAgent` to load a Jinja2 template from a file. This allows for more flexible and maintainable prompts by separating the prompt structure from the agent's code.

## CODEBASE ANALYSIS
The `ProjectAnalysisAgent` in `agents/project_analysis_agent/agent.py` is responsible for analyzing the project. It currently constructs a prompt string directly within the `execute` method. This feature will introduce a new method, `_load_template`, to load the template from `agents/project_analysis_agent/templates/project_analysis_template.md`. The `execute` method will be updated to use this template to generate the analysis prompt.

## DOMAIN RESEARCH
Using templates for prompts is a standard practice in applications that generate text from structured data. It improves maintainability, readability, and allows for easier updates to the prompt without changing the code. Jinja2 is a common and powerful templating engine for Python.

## TECHNICAL APPROACH
The recommended approach is to add a `_load_template` method to the `ProjectAnalysisAgent`. This method will take a template name as input, read the corresponding file from the `templates` directory, and return a Jinja2 Template object. The `execute` method will then call this new method to get the template and render it with the required context variables.

An alternative would be to keep the template as a string within the agent, but this is less maintainable and harder to scale.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
The `ProjectAnalysisAgent` will be modified.

## RISK ASSESSMENT
### Technical Risks
- **Jinja2 Dependency**: The project will now depend on the Jinja2 library. This is a low risk as Jinja2 is a well-maintained and widely used library.
    - **Mitigation**: Add Jinja2 to `requirements.txt`.
- **Template Not Found**: The template file might be missing or in the wrong location.
    - **Mitigation**: The `_load_template` method should include error handling to catch `FileNotFoundError` and provide a clear error message.

### Business Risks
None.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: enhancement

## IMPLEMENTATION DETAILS
- **Files to modify**:
    - `agents/project_analysis_agent/agent.py`: Add the `_load_template` method and update the `execute` method.
    - `requirements.txt`: Add the `Jinja2` dependency.
- **Key classes/functions to implement**:
    - `ProjectAnalysisAgent._load_template(self, template_name: str) -> Template:`
- **Acceptance criteria**:
    - The `ProjectAnalysisAgent` successfully loads the `project_analysis_template.md` file.
    - The agent uses the loaded template to generate the analysis prompt.
    - The final prompt is correctly rendered with the project data.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Adding a method to load a Jinja2 template from a file.
- Updating the `execute` method to use the loaded template.
- Adding Jinja2 to the project dependencies.

**OUT OF SCOPE**:
- Implementing more complex template logic like inheritance or macros.
- Creating a generic template loading mechanism for all agents.

## ACCEPTANCE CRITERIA
- [ ] The `ProjectAnalysisAgent` can load a template from a file.
- [ ] The `execute` method uses the template to generate the prompt.
- [ ] The Jinja2 dependency is added to `requirements.txt`.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add basic template loading to ProjectAnalysisAgent
**Labels**: enhancement, project-analysis
**Assignee**:
**Project**: Loom Phase 1