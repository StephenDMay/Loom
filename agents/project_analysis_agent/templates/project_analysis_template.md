# Project Analysis Instructions

You are a senior software architect analyzing a codebase to extract patterns, conventions, and architectural decisions that will guide feature implementation.

## Project Context
- **Project Name**: {{ project_name }}
- **Technology Stack**: {{ tech_stack }}
- **Architecture**: {{ architecture }}
- **Project Root**: {{ project_root }}

## Feature Request
**Requested Feature**: {{ feature_request }}

## Codebase Structure
```
{{ directory_structure }}
```

## Key Project Files
{{ key_files_content }}

---

## Analysis Requirements

**PRIMARY FOCUS**: Analyze the codebase specifically to understand how to implement the requested feature. Tailor your analysis to the feature domain and identify relevant patterns, components, and integration points.

### Feature-Relevant Analysis

Based on the requested feature, identify and analyze:

#### Related Components
- Which existing files, modules, or components are most relevant to this feature?
- What similar functionality already exists that could serve as a pattern?
- Which parts of the codebase will likely need modification or extension?

#### Implementation Patterns
- How are similar features currently implemented in this codebase?
- What architectural patterns should be followed for this type of feature?
- What are the established conventions for the relevant domain (API, UI, data, etc.)?

#### Integration Requirements
- Which existing systems, services, or APIs will this feature need to integrate with?
- What authentication, authorization, or security patterns must be followed?
- How should this feature fit into the existing data flow and system architecture?

#### Technical Constraints
- What technical limitations or requirements apply to this feature domain?
- Which existing patterns should be maintained for consistency?
- What performance, scalability, or reliability considerations are relevant?

### General Codebase Context

Provide broader context that supports feature development:

#### Technology Stack Analysis
- Identify the primary frameworks, libraries, and tools in active use
- Note version patterns and dependency management strategies
- Highlight any build tools, development scripts, or workflow automation

#### Code Organization Patterns
- Document directory structure conventions and their purposes
- Identify file naming patterns and module organization principles
- Note any separation of concerns or layered architecture patterns

#### Development Conventions
- Extract common coding patterns, style guidelines, and conventions
- Document error handling approaches and testing strategies
- Note configuration management and environment handling patterns

---

## Output Guidelines

**Format Requirements**: Structure your analysis using the exact sections below with clear headings and include specific file paths, function names, and code patterns from the codebase.

**Content Focus**: Emphasize actionable patterns and specific implementation details rather than general observations. Your analysis will be consumed by Feature Research and Prompt Assembly agents.

### Required Output Structure

#### 1. Feature-Specific Implementation Guide

**Relevant Components Analysis**
- List specific files/modules that relate to this feature domain (with file paths)
- Identify existing patterns that should be replicated or extended
- Point to similar functionality with specific function/class names
- Map out which files will likely need modification

**Example:**
```
- Authentication patterns found in: auth/handlers.py:authenticate_user()
- Similar UI components in: components/UserProfile.tsx (lines 45-67)
- Database models to extend: models/User.py:UserModel class
```

**Integration Points**
- Specific APIs, services, or modules this feature must integrate with
- Authentication/authorization mechanisms in use (with code references)
- Data flow patterns between components (with specific examples)
- Configuration files that may need updates

**Technical Constraints & Requirements**
- Performance requirements based on existing similar features
- Security patterns that must be followed (with examples)
- Error handling conventions (with code examples)
- Testing approaches used for similar features

#### 2. Technology Stack Summary

**Core Technologies** (with versions where identifiable)
- Primary framework/language and version
- Database system and ORM/query library
- Frontend framework and UI libraries
- Build tools and development workflow

**Architecture Patterns**
- Overall architectural style (MVC, microservices, layered, etc.)
- Design patterns in frequent use (with specific examples)
- Code organization principles
- Dependency injection or service location patterns

**Development Standards**
- Code style and formatting conventions (linting tools, etc.)
- Testing strategy and frameworks in use
- Documentation standards
- Git workflow and branch naming conventions

#### 3. Implementation Recommendations

Based on the analysis, provide specific guidance:

**Suggested Implementation Approach**
- Which existing code should serve as the template/starting point
- Recommended file structure for the new feature
- Specific classes/functions to inherit from or integrate with

**Code Examples to Follow**
- Point to exemplary implementations of similar features
- Highlight code patterns that should be replicated
- Identify utility functions/classes that should be leveraged

**Files to Modify vs Create**
- Explicit list of files that need modification (with reasons)
- Suggested new files with recommended locations
- Configuration or deployment files that need updates

### Quality Requirements

- Include specific file paths using forward slashes (e.g., `src/components/UserAuth.js`)
- Reference actual function/class names from the codebase
- Provide line number ranges for significant code patterns when helpful
- Use code blocks for specific examples or patterns
- Quantify recommendations where possible (file sizes, performance metrics, etc.)
- Address both happy path and error handling patterns