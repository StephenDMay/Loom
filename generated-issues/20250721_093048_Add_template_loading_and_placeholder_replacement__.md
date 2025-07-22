# FEATURE: Add template loading and placeholder replacement to ProjectAnalysisAgent

## EXECUTIVE SUMMARY
This feature will enable the `ProjectAnalysisAgent` to load a template file, replace placeholders with dynamic data, and use the result as a prompt for the LLM. This makes the agent's analysis more structured, configurable, and tailored to specific analysis tasks.

## CODEBASE ANALYSIS
- **`agents/project_analysis_agent/agent.py`**: This is the core file for the `ProjectAnalysisAgent`. It currently constructs a hardcoded prompt string. This will be modified to load a template, replace placeholders, and use the result as the prompt.
- **`agents/project_analysis_agent/templates/project_analysis_template.md`**: This file contains the template to be used for the analysis prompt. It includes placeholders like `{{ project_name }}` and `{{ directory_structure }}`.
- **`core/context_manager.py`**: The `ContextManager` is used to store the results of the analysis. The agent already interacts with it, and this interaction will be maintained.
- **`agents/project_analysis_agent/config.json`**: The agent's configuration file. We will add a new key `template_file` to specify the path to the template.

## DOMAIN RESEARCH
- **User Workflows**: Developers often need to perform different types of analysis on a codebase. Using templates allows them to define various analysis "recipes" without changing the agent's code. For example, one template could be for a general overview, while another could be for a security-focused analysis.
- **Industry Patterns**: Template engines (like Jinja2, Mustache, etc.) are a standard way to separate presentation/structure from content/data. This feature implements a simple version of that pattern.
- **Competitive Analysis**: Many code analysis tools and CI/CD pipelines use templates (e.g., GitHub Actions workflows, Jenkinsfiles) to define reusable processes.

## TECHNICAL APPROACH
The recommended approach is to:
1.  Add a `template_file` key to the `project_analysis_agent` section of `agents/project_analysis_agent/config.json`.
2.  In the `ProjectAnalysisAgent`'s `__init__` method, read the `template_file` path from the config.
3.  Create a new private method, `_load_and_prepare_template`, that takes the dynamic data (directory structure, key file content, etc.) as input.
4.  This new method will read the template file from the path specified in the config.
5.  It will then iterate through a dictionary of placeholders and their corresponding values, replacing each placeholder in the template string.
6.  The `execute` method will be updated to call this new method to get the final prompt to be sent to the LLM.

An alternative approach would be to use a more powerful template engine like Jinja2. However, for the current scope, simple string replacement is sufficient and avoids adding a new dependency.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required.

### API Design
No API changes are required.

### Frontend Components
No frontend components are involved.

### Backend Services
- **`ProjectAnalysisAgent`**:
    - A new private method `_load_and_prepare_template(self, context: Dict[str, str]) -> str` will be added.
    - The `execute` method will be modified to use this new method to generate the LLM prompt.
- **Configuration**:
    - `agents/project_analysis_agent/config.json` will be updated to include a `template_file` path.

## RISK ASSESSMENT
### Technical Risks
- **Template Not Found**: The specified template file might not exist.
    - **Mitigation**: The agent should handle this gracefully, logging an error and falling back to the old hardcoded prompt or raising an exception.
- **Missing Placeholders**: The template might contain placeholders for which the agent doesn't have data.
    - **Mitigation**: The agent should be robust to this, perhaps replacing them with an empty string or a "not available" message.

### Business Risks
- **Incorrectly Formatted Templates**: Users might create templates that are not well-formed, leading to poor analysis results.
    - **Mitigation**: Provide clear documentation and examples of how to create templates.

## PROJECT DETAILS
**Estimated Effort**: 1 day
**Dependencies**: None
**Priority**: High
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to modify**:
    - `agents/project_analysis_agent/agent.py`
    - `agents/project_analysis_agent/config.json`
- **Key classes/functions to implement**:
    - `ProjectAnalysisAgent._load_and_prepare_template(self, context: Dict[str, str]) -> str`
- **Exact CLI command structure**: No new CLI commands are introduced.
- **Clear acceptance criteria for "done"**:
    - The agent loads the template specified in the config.
    - The agent replaces placeholders in the template with the correct data.
    - The agent sends the processed template content to the LLM.
    - If the template file is not found, the agent logs an error and does not crash.

## SCOPE BOUNDARIES
**IN SCOPE**:
- Loading a template file from a path specified in the config.
- Replacing placeholders in the format `{{ placeholder_name }}` with data available within the agent.
- Using the processed template as the prompt for the LLM.

**OUT OF SCOPE**:
- Implementing a full-featured templating engine with logic, loops, etc.
- Dynamic loading of templates from multiple locations.
- A UI for managing templates.

## ACCEPTANCE CRITERIA
- [ ] The `ProjectAnalysisAgent` reads the `template_file` path from its configuration.
- [ ] The agent successfully loads the content of the specified template file.
- [ ] The agent replaces placeholders like `{{ directory_structure }}` and `{{ key_files_content }}` with the corresponding data.
- [ ] The final prompt sent to the LLM is the result of this template processing.
- [ ] The system handles the case where the template file does not exist by logging an error.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add template loading and placeholder replacement to ProjectAnalysisAgent
**Labels**: enhancement, project-analysis
**Assignee**:
**Project**: Loom Phase 1
I will now implement the changes. First, I'll modify the config file.