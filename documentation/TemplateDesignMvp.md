# MVP Template System Features

## Week 1: Core Template System (MVP Essentials)

### TASK-001: Add basic template loading to ProjectAnalysisAgent **DONE** ✅
**Effort**: 6-8 hours
- Create `agents/project_analysis_agent/templates/project_analysis_template.md` with the feature-focused content ✅
- Add `_load_and_prepare_template()` method with file reading and regex-based placeholder replacement ✅
- Template processing with dynamic context replacement ✅
- **MVP Goal**: Agent can load and use a template instead of hardcoded prompts ✅
- **Implementation**: `agents/project_analysis_agent/agent.py:121-155`

### TASK-002: Pass feature request to ProjectAnalysisAgent **DONE** ✅
**Effort**: 3-4 hours
- Update agent's `execute()` method to accept `feature_request` parameter ✅
- Add `{{ feature_request }}` placeholder to template processing ✅
- Context includes feature request in template rendering ✅
- **MVP Goal**: Template gets populated with actual feature request ✅
- **Implementation**: `agents/project_analysis_agent/agent.py:157-184`

### TASK-003: Create minimal FeatureResearchAgent template **DONE** ✅
**Effort**: 4-5 hours
- Create `agents/feature_research_agent/templates/feature_research_template.md` with dynamic context handling ✅
- Implement template loading pattern with `_load_template()` and `_render_template()` methods ✅
- Focus on dynamic context discovery and inclusion ✅
- **MVP Goal**: Second agent uses templates and previous agent output ✅
- **Implementation**: `agents/feature_research_agent/agent.py:22-84`

### TASK-004: Create minimal PromptAssemblyAgent template **DONE** ✅
**Effort**: 4-5 hours
- Create `agents/prompt_assembly_agent/templates/example_template.md` that aggregates all context ✅
- Template combines all available context into final output with file generation ✅
- Focus on comprehensive context synthesis and file output ✅
- **MVP Goal**: Final agent produces template-driven coding prompt ✅
- **Implementation**: `agents/prompt_assembly_agent/agent.py:28-302`

-------------------------------------------------------------------------------------
# Revised Feature Specifications: LLM-Driven Context Interpretation

## Core Philosophy Shift

**OLD**: Agents have rigid context contracts and dependencies
**NEW**: LLMs interpret available context intelligently through templates

## Revised Agent Behaviors

### FeatureResearchAgent (Features 10-12)

**FEATURE-010: Create FeatureResearchAgent class structure** ⭐ HIGH PRIORITY  **DONE**
- Create `agents/feature_research_agent/agent.py` and `manifest.json`
- Implement `execute(feature_request: str)` method that opportunistically reads context
- NO required context dependencies - agent works standalone or enhanced
- **Scope**: New agent file structure, context discovery logic, ~60 lines

**FEATURE-011: Add context-aware research logic to FeatureResearchAgent** ⭐ HIGH PRIORITY **DONE**
- Implement `_gather_available_context()` method for opportunistic context discovery
- Build research prompt that includes whatever context is available
- LLM interprets context relevance and fills gaps intelligently
- **Scope**: Context gathering + prompt building logic, ~40-50 lines

**FEATURE-012: Add research template with smart context handling** ⭐ HIGH PRIORITY **DONE**
- Create `feature_research_template.md` with conditional context sections
- Template includes context when available, provides fallbacks when missing
- LLM given explicit instructions to work with partial information
- **Scope**: Template file + template processing logic, ~30 lines code + template

### PromptAssemblyAgent (Features 13-15)

**FEATURE-013: Create PromptAssemblyAgent class structure** ⭐ HIGH PRIORITY **DONE**
- Create `agents/prompt_assembly_agent/agent.py` and `manifest.json` 
- Implement `execute(feature_request: str)` method that scavenges all available context
- Agent becomes context aggregator rather than context receiver
- **Scope**: New agent file structure, context aggregation logic, ~60 lines
- **Implementation**: `agents/prompt_assembly_agent/agent.py:13-26`

**FEATURE-014: Add intelligent context compilation to PromptAssemblyAgent** ⭐ HIGH PRIORITY **DONE**
- Implement context discovery that finds ALL available context keys
- Build comprehensive prompt from whatever agents have contributed
- LLM decides how to weight and integrate different context sources
- **Scope**: Context compilation + prompt optimization logic, ~50-60 lines
- **Implementation**: `agents/prompt_assembly_agent/agent.py:192-217`

**FEATURE-015: Add assembly template with maximum context flexibility** ⭐ HIGH PRIORITY **DONE**
- Create `prompt_assembly_template.md` that dynamically includes available context
- Template gives LLM control over how to synthesize information
- Final prompt quality improves based on available context richness
- **Scope**: Template file + dynamic context injection, ~40 lines code + template
- **Implementation**: `agents/prompt_assembly_agent/templates/example_template.md`

## Template-Driven Intelligence Examples

### Feature Research Template Structure:
```markdown
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
```

### Prompt Assembly Template Structure:
```markdown
# Final Coding Prompt Assembly

You are assembling the ultimate coding prompt from multiple research sources.

## Original Request
{{ feature_request }}

## Research Synthesis
{% for agent_output in context_outputs %}
### {{ agent_output.agent_name|title }} Analysis
{{ agent_output.content }}

{% endfor %}

## Assembly Instructions
Create a comprehensive coding prompt that:
1. Synthesizes all available research into coherent implementation guidance
2. Prioritizes information based on relevance and quality
3. Provides clear, actionable implementation steps
4. Includes specific technical details and code examples where possible

**Quality Standards:**
- Prefer specific over general guidance
- Include concrete implementation details
- Provide fallback approaches for uncertain areas
- Ensure prompt is self-contained and actionable
```

## Key Benefits

1. **Zero Configuration Overhead**: No context contracts for users to maintain
2. **LLM Intelligence**: Models decide how to interpret and synthesize context
3. **Template Control**: Users control output through template modification, not config
4. **Graceful Degradation**: Quality improves with more context, but works with less
5. **Future-Proof**: New agents automatically enhance existing agents' context

## Implementation Strategy

Each agent becomes a context-opportunistic LLM prompter:
- Discover what context exists
- Build intelligent prompts that include available context
- Let LLMs interpret relevance and fill gaps
- Store results for downstream agents to discover

This shifts complexity from configuration to template design, where users have direct control over the intelligence and output quality.