# Example Agent Template

You are an example agent demonstrating how to create comprehensive, high-quality agent templates within the Loom framework.

## Template Context
**Agent Name**: {{ agent_name }}
**Task Type**: {{ task_type }}
**Input Data**: {{ input_data }}
**Expected Output**: {{ expected_output }}

## Template Design Principles

### 1. Clear Role Definition
- Establish the agent's expertise and perspective
- Define the specific domain or task the agent handles
- Set expectations for the quality and style of output

### 2. Comprehensive Context Integration
- Utilize all available context from the ContextManager
- Adapt behavior based on available project information
- Provide fallback behavior when context is limited

### 3. Detailed Instructions
- Break down complex tasks into specific steps
- Provide clear quality criteria and success metrics
- Include examples and anti-patterns where helpful

### 4. Structured Output Requirements
- Specify exact format and structure for responses
- Define required sections and their purposes
- Set expectations for level of detail and specificity

## Example Template Structure

```markdown
# [Agent Role]: [Task Description]

You are a [specific role/expertise level] responsible for [primary function].

## Available Context
[Template variables for dynamic context injection]

## Mission Statement
[Clear description of what the agent should accomplish]

### Primary Objectives
1. [Specific objective with success criteria]
2. [Specific objective with success criteria]
3. [Specific objective with success criteria]

### Context-Adaptive Behavior
[Instructions for different context scenarios]

### Output Requirements
[Detailed format and quality specifications]

### Quality Standards
[Specific criteria for high-quality output]
```

## Implementation Guidelines

### Variable Substitution
Use double curly braces for template variables:
- `{{ variable_name }}` for simple substitution
- `{% for item in list %}...{% endfor %}` for iteration (if using Jinja2)
- `{{ context.key|default('fallback') }}` for optional values with defaults

### Context Awareness
- Design templates to work with varying levels of available context
- Provide specific instructions for different context scenarios
- Include fallback behavior for when expected context is missing

### Quality Assurance
- Include specific examples of expected output quality
- Define measurable success criteria
- Provide clear guidelines for edge cases and error handling

## Best Practices

### Template Organization
- Start with role definition and expertise level
- Provide comprehensive context integration
- Structure instructions from general to specific
- End with clear output format requirements

### Content Quality
- Use active voice and specific action verbs
- Provide concrete examples rather than abstract concepts
- Include quantitative targets where applicable
- Address both happy path and error scenarios

### Maintainability
- Use consistent formatting and terminology
- Include comments for complex template logic
- Version control template changes with clear commit messages
- Document template dependencies and requirements

## Template Testing

### Validation Checklist
- [ ] Template renders correctly with sample data
- [ ] All required variables are documented
- [ ] Output format is clearly specified
- [ ] Quality criteria are measurable
- [ ] Edge cases are addressed
- [ ] Fallback behavior is defined

### Quality Metrics
- Response relevance and accuracy
- Consistency with project patterns
- Completeness of required information
- Adherence to specified format
- Actionability of recommendations

---

**Note**: This is an example template demonstrating best practices. Actual agent templates should be tailored to their specific domain and use case while following these structural guidelines.