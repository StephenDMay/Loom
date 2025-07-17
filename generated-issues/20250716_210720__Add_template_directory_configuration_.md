# FEATURE: Add template directory configuration

## EXECUTIVE SUMMARY
This feature introduces a configurable mechanism to specify template directories within the `dev-automation.config.json` file. This allows users to define custom locations for templates, enhancing flexibility and enabling easier management of project-specific or user-defined templates without modifying the core application structure.

## CODEBASE ANALYSIS
The `dev-automation.config.json` file currently has an empty `"templates": {}` section, which is an ideal location for this new configuration. The `core/config_manager.py` provides robust methods for loading, merging, and retrieving configuration values, including nested keys, which will be leveraged. The `agents/issue_generator/agent.py` currently hardcodes the path to `meta-prompt-template.md` relative to the project root. This agent will be modified to use the new configurable template directories to locate the meta-prompt template. Other template files in the `templates/` directory (e.g., `api.py`, `data.py`) are not currently used by the `IssueGeneratorAgent`, so the initial scope will focus on making the `meta-prompt-template.md` path configurable.

## DOMAIN RESEARCH
Users often require flexibility in managing configuration and resource files. Allowing configurable template directories aligns with best practices for extensible tools, enabling developers to:
- Store templates in a central location outside the project if desired.
- Override default templates with project-specific versions.
- Share templates across multiple projects.
Common patterns involve specifying a list of paths, which are then searched in order until the desired file is found. This provides a clear resolution hierarchy.

## TECHNICAL APPROACH
The recommended approach is to add a new configuration key, `templates.directories`, as a list of strings in `dev-automation.config.json`. Each string in this list will represent an absolute or relative path to a directory containing templates. The `IssueGeneratorAgent` will be updated to iterate through these configured directories, resolving relative paths against the project root, to locate the `meta-prompt-template.md` file. The first instance of the template found in the specified order will be used.

## IMPLEMENTATION SPECIFICATION
### Database Changes
No database changes are required as this feature involves file-based configuration.

### API Design
No new API endpoints are required. The `ConfigManager`'s existing `get` method will be used to retrieve the `templates.directories` list.

### Frontend Components
No frontend components are involved as this is a CLI tool.

### Backend Services
- **`core/config_manager.py`**: No direct code changes are needed here, as the existing `get` method can handle retrieving the new configuration.
- **`agents/issue_generator/agent.py`**:
    - Modify the `__init__` method to retrieve the `templates.directories` list from the `ConfigManager`.
    - Implement a new helper method, e.g., `_find_template_path(template_name: str) -> Path | None`, which iterates through the configured directories, constructs the full path for the template, and checks for its existence.
    - Update the `execute` method to use this new helper method to locate `meta-prompt-template.md`.

## RISK ASSESSMENT
### Technical Risks
- **Invalid Paths**:
    - Description: Users might provide invalid or non-existent paths in the `templates.directories` configuration.
    - Mitigation: Implement robust error handling in the `_find_template_path` method. Log warnings for invalid paths and skip them, ensuring the system continues to function by trying subsequent paths or falling back to a default if no valid template is found.
- **Performance Impact**:
    - Description: Searching through a large number of configured directories could introduce a minor performance overhead.
    - Mitigation: For the expected number of template directories (likely small), the impact should be negligible. If performance becomes an issue with many directories, caching mechanisms could be considered in the future.
- **Ambiguous Template Names**:
    - Description: If the same template name (e.g., `meta-prompt-template.md`) exists in multiple configured directories, it could lead to confusion about which one is being used.
    - Mitigation: Clearly define and document the search order (e.g., "first found wins"). This is a standard and predictable approach.

### Business Risks
- **User Confusion**:
    - Description: If the template resolution logic is not clear or if error messages are unhelpful, users might struggle to configure their template directories correctly.
    - Mitigation: Provide clear documentation on how to configure `templates.directories` and ensure error messages are informative (e.g., "Template 'X' not found in any configured directories: [list of paths searched]").

## PROJECT DETAILS
**Estimated Effort**: 1-2 days
**Dependencies**: None
**Priority**: Medium
**Category**: Feature/Enhancement

## IMPLEMENTATION DETAILS
- **Specific files to create/modify**:
    - `C:/Users/Steve/Projects/AutoDev/dev-automation.config.json`
    - `C:/Users/Steve/Projects/AutoDev/agents/issue_generator/agent.py`
- **Key classes/functions to implement**:
    - In `agents/issue_generator/agent.py`:
        - Modify `__init__` to store `self.template_directories = self.config.get('templates.directories', [])`
        - Add a new method `_find_template_path(self, template_name: str) -> Path | None`
        - Update `execute` method to call `self._find_template_path("meta-prompt-template.md")`
- **Exact CLI command structure**:
    - The CLI command `python dev-issue.py "feature description"` remains unchanged. The configuration is handled via `dev-automation.config.json`.
- **Clear acceptance criteria for "done"**: See ACCEPTANCE CRITERIA section below.

## SCOPE BOUNDARIES
**What is explicitly IN scope for this feature?**
- Adding a `templates.directories` list to `dev-automation.config.json`.
- Modifying `IssueGeneratorAgent` to search for `meta-prompt-template.md` within the configured directories.
- Resolving relative paths in `templates.directories` against the project root.
- Implementing basic error handling for non-existent template directories or files.

**What is explicitly OUT of scope and should be separate features?**
- A comprehensive template management system (e.g., listing all available templates, dynamic selection of templates beyond `meta-prompt-template.md`).
- Support for different template engines (e.g., Jinja2, Handlebars).
- UI for managing template directories.
- Automatic downloading or fetching of templates from remote sources.

## ACCEPTANCE CRITERIA
- [X] The `dev-automation.config.json` file can be updated with a `templates.directories` key containing a list of paths.
- [X] The `IssueGeneratorAgent` successfully loads `meta-prompt-template.md` from a directory specified in `templates.directories`.
- [X] If multiple directories are specified in `templates.directories`, the `IssueGeneratorAgent` uses the `meta-prompt-template.md` found in the first directory in the list.
- [X] Relative paths provided in `templates.directories` are correctly resolved against the project root.
- [X] If `meta-prompt-template.md` is not found in any configured directory, the system provides a clear error message and falls back to a default behavior (e.g., using the hardcoded path if it exists, or exiting with an error).
- [X] The system handles cases where a directory in `templates.directories` does not exist gracefully (e.g., logs a warning and skips it).

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add configurable template directories
**Labels**: enhancement, configuration, templates
**Assignee**: (if known)
**Project**: AutoDev-Board
