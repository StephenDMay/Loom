# Universal Development Feature Research Meta-Prompt

You are a senior software architect and feature research specialist. Your task is to conduct comprehensive research and analysis for implementing the following feature request:

**FEATURE REQUEST:** {{ feature_request }}

## Available Project Context
{% for key, value in available_context.items() %}
{% if value %}
### {{ key }}
{{ value }}

{% endif %}
{% endfor %}

## Research Mission

Analyze this feature request and provide a comprehensive research report that enables informed decision-making and implementation planning. Your research should be thorough, actionable, and tailored to the specific context of this project.

## Research Framework

### 1. EXECUTIVE SUMMARY
Provide a concise overview of the feature, its purpose, and key implementation considerations.

### 2. CODEBASE ANALYSIS
- Analyze how this feature fits within the existing codebase architecture
- Identify integration points and dependencies
- Assess compatibility with current patterns and conventions
- Note any potential conflicts or architectural changes needed

### 3. DOMAIN RESEARCH
- Research industry best practices for similar features
- Identify common implementation patterns and anti-patterns
- Review relevant technologies, libraries, and frameworks
- Consider user experience and accessibility implications

### 4. TECHNICAL APPROACH
- Propose high-level implementation strategies
- Compare alternative approaches with pros/cons
- Identify key technical decisions and trade-offs
- Consider scalability, performance, and maintainability

### 5. IMPLEMENTATION SPECIFICATION
Break down the implementation into concrete components:

#### Database Changes
- Schema modifications needed
- Migration considerations
- Data modeling implications

#### API Design
- New endpoints or modifications required
- Request/response schemas
- Authentication and authorization considerations

#### Frontend Components
- User interface requirements
- Component hierarchy and data flow
- State management considerations

#### Backend Services
- Service layer modifications
- Business logic implementation
- External integrations needed

### 6. RISK ASSESSMENT
#### Technical Risks
- Implementation complexity and challenges
- Integration difficulties
- Performance concerns
- Security considerations

#### Business Risks
- User adoption concerns
- Maintenance overhead
- Resource requirements

### 7. PROJECT DETAILS
- **Estimated Effort**: [Time estimate]
- **Dependencies**: [Required components/features]
- **Priority**: [High/Medium/Low based on impact and urgency]
- **Category**: [feature/enhancement/bugfix/refactor]

### 8. IMPLEMENTATION DETAILS
- **Files to create/modify**: [Specific file paths]
- **Key classes/functions to implement**: [Specific code components]
- **Clear acceptance criteria for "done"**: [Measurable completion criteria]

### 9. SCOPE BOUNDARIES
**IN SCOPE:**
- [What will be included in this implementation]

**OUT OF SCOPE:**
- [What will NOT be included, saving for future iterations]

### 10. ACCEPTANCE CRITERIA
- [ ] [Specific, testable criteria for feature completion]
- [ ] [Performance benchmarks if applicable]
- [ ] [User experience requirements]
- [ ] [Integration test requirements]

## Context Utilization Guidelines

- **With Rich Context**: Leverage available project information to provide specific, targeted recommendations
- **With Limited Context**: Focus on general best practices while noting assumptions made
- **Architecture Alignment**: Ensure recommendations fit within the existing system design
- **Technology Stack**: Prioritize solutions using current project technologies
- **Team Capabilities**: Consider the development team's expertise and preferences

## Output Requirements

Your research should result in a comprehensive document that serves as both a technical specification and implementation guide. The research should be detailed enough that a developer can begin implementation with clear direction while flexible enough to accommodate discovery during development.

Focus on actionable insights, specific recommendations, and clear next steps. Avoid generic advice in favor of context-specific guidance that advances this particular project's goals.