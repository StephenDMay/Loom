# Feature Research Instructions

You are researching implementation approaches for: {{ feature_request }}

## Available Project Context
{% for key, value in available_context.items() %}
{% if value %}
### {{ key|title }}
{{ value }}
{% endif %}
{% endfor %}

## Research Mission
Provide comprehensive implementation research. Use available context to tailor your research, but provide valuable insights even if context is limited.

**Key Areas to Research:**
- Implementation patterns and best practices
- Integration considerations (adapt based on available context)
- Technical requirements and constraints
- Similar feature examples and approaches

**Context Interpretation Instructions:**
- If project analysis is available, focus research on integration points
- If codebase structure is known, align with existing patterns
- If no context available, provide general best practices
- Always provide actionable implementation guidance