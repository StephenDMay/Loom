# FEATURE: Readable and Searchable Issue Filenames

## EXECUTIVE SUMMARY
This feature improves the developer experience by changing the naming convention for generated issue files. The new format, `YYYY-MM-DD-HHMMSS-feature-title-slug.md`, is more readable, descriptive, and easier to search than the current timestamp-prefixed format, making it faster for developers to locate specific issue files.

## CODEBASE ANALYSIS
- **Relevant Component**: `agents/issue_generator/agent.py` is the sole component responsible for generating the issue files and their names.
- **Current Logic**: The filename is generated using `f"{timestamp}_{safe_feature}.md"`, where `timestamp` is `YYYYMMDD_HHMMSS` and `safe_feature` is a truncated, underscore-sanitized version of the initial user prompt.
- **Integration Points**: A search of the codebase reveals no programmatic dependencies on the current filename format. The only references are in the `README.md` as an example command and within the content of an already-generated issue, neither of which will cause a runtime failure.
- **Impact**: The change is isolated to the `IssueGeneratorAgent`'s `execute` method. The primary impact is on the final output file name.

## DOMAIN RESEARCH
- **User Workflow**: Developers run the agent to generate a feature specification. They then browse the `generated-issues/` directory to find the relevant file.
- **Pain Point**: The current format `20250818_213635_update_readme_to_reflect_the_new_architecture_and_.md` makes it difficult to identify a file's content without opening it. The timestamp dominates the name, and the title is truncated and poorly formatted.
- **Industry Best Practices**: Common practice for content-driven file generation (like static site blogs or documentation) is to use a "slug" derived from the title (e.g., `a-guide-to-better-filenames.md`). Combining this with a date for uniqueness and sorting is also standard (e.g., `2025-08-18-a-guide-to-better-filenames.md`).

## TECHNICAL APPROACH
The recommended approach is to modify the file-saving logic within `agents/issue_generator/agent.py` to occur *after* the LLM has generated the content.

1.  **Generate Content**: Execute the LLM call and receive the raw markdown result.
2.  **Extract Title**: Parse the markdown result to find the feature title (e.g., the line starting with `# FEATURE:`).
3.  **Create Slug**: Implement a "slugify" utility to convert the title into a URL-friendly, kebab-case string (e.g., "Make Filenames Readable" -> "make-filenames-readable"). This involves lowercasing, removing special characters, and replacing spaces with hyphens.
4.  **Construct New Filename**: Combine a readable timestamp (`YYYY-MM-DD-HHMMSS`) with the new slug to create the final filename. This maintains uniqueness and chronological sorting while vastly improving readability.
5.  **Save File**: Write the LLM-generated content to the newly named file.

An alternative would be to omit the timestamp, but this increases the risk of filename collisions if two features have similar titles. The proposed timestamp-slug combination is a robust and user-friendly solution.

## IMPLEMENTATION SPECIFICATION
### Database Changes
None.

### API Design
None.

### Frontend Components
None.

### Backend Services
The `IssueGeneratorAgent` service will be modified. No other services are affected.

## RISK ASSESSMENT
### Technical Risks
- **Risk 1**: Historical references in old generated files will point to non-existent filenames.
  - **Mitigation**: This is an acceptable risk. The primary value is in the content of the old files, not their metadata. We will not retroactively rename old files.
- **Risk 2**: A bug in the title extraction or slugify logic could lead to poorly formatted or non-unique filenames.
  - **Mitigation**: The logic should be simple and include robust fallbacks. If no title is found, the agent can revert to the old naming scheme using the user's prompt to prevent errors.

### Business Risks
- **Risk 1**: Developers accustomed to the old format may be briefly disoriented.
  - **Mitigation**: The new format is objectively more intuitive. A brief mention in project communications or the `README.md` will be sufficient.

## PROJECT DETAILS
**Estimated Effort**: 0.5 days
**Dependencies**: None
**Priority**: Medium
**Category**: enhancement

## IMPLEMENTATION DETAILS
- **Files to Modify**:
    - `agents/issue_generator/agent.py`: To implement the new filename generation logic.
    - `README.md`: To update the example `gh issue create` command to reflect the new filename format.

- **Key Functions to Implement**:
    - A new private method `_extract_title_from_markdown(content: str) -> str` in `IssueGeneratorAgent`.
    - A new private method `_slugify(text: str) -> str` in `IssueGeneratorAgent`.
    - The file generation logic inside the `execute` method will be moved to after the `self.llm_manager.execute()` call.

- **CLI Command Structure**: No change to any CLI commands.

## SCOPE BOUNDARIES
- **IN Scope**:
    - Changing the filename generation logic for all new issues created by the `IssueGeneratorAgent`.
    - Updating the `README.md` to reflect the new format.
- **OUT of Scope**:
    - Renaming any existing files in the `generated-issues/` directory.
    - Creating a script to migrate old filenames.

## ACCEPTANCE CRITERIA
- [ ] When the `IssueGeneratorAgent` is run, the output file is saved in the `generated-issues/` directory.
- [ ] The filename format is `YYYY-MM-DD-HHMMSS-[slug].md`.
- [ ] The `[slug]` part of the filename is a clean, kebab-case version of the feature title from the generated markdown content.
- [ ] If a feature title cannot be parsed from the content, the system gracefully falls back to a safe, timestamp-based name.
- [ ] The example command in `README.md` is updated to show the new filename convention.

## GITHUB ISSUE TEMPLATE
**Title**: Enhance: Improve Readability of Generated Issue Filenames
**Labels**: enhancement, developer-experience
**Assignee**:
**Project**: Loom Development