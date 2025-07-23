# Auto-Dev Architecture & Design Decisions

## System Overview

Auto-dev is a multi-agent system that transforms feature requests into comprehensive coding prompts through LLM-driven sequential analysis. The system uses opportunistic context discovery and template-driven intelligence to enable flexible, plug-and-play agent collaboration without configuration overhead.

## Core Architecture Philosophy

### LLM-Driven Intelligence
**Principle**: Shift complexity from configuration to template-driven LLM interpretation
- **Templates** contain the intelligence and user control surface
- **LLMs** handle context synthesis, gap filling, and relevance determination  
- **Agents** become thin wrappers around intelligent template execution
- **Users** control behavior through template modification, not configuration

### Opportunistic Context Discovery
**Principle**: Agents are context-aware, not context-dependent
- Agents scavenge available context via `context_manager.get()`
- Quality improves with more context, but agents work with less
- No rigid dependencies between agents
- Progressive enhancement through emergent collaboration

### Zero Configuration Overhead
**Principle**: Intelligence emerges from template design, not configuration complexity
- No context contracts for users to maintain
- Plug-and-play agent addition without configuration changes
- Sensible defaults with template-driven customization
- Future-proof architecture that adapts to new agents automatically

---

## Architectural Decisions

### Context Discovery Strategy ✅ DECIDED

**Question**: How should agents access and share context - through structured contracts, direct passing, or opportunistic discovery?

**Decision**: **Opportunistic Context Discovery with LLM Interpretation**

**Rationale**:
- **Zero Configuration Overhead**: No context contracts for users to maintain
- **LLM Intelligence**: Models interpret available context and fill gaps intelligently
- **Template Control**: Users control intelligence through template modification, not config
- **Graceful Degradation**: Quality improves with more context, works with less
- **Future-Proof**: New agents automatically enhance existing agents' context
- **Plug-and-Play**: Agents become context-aware without rigid dependencies

**Implementation**: Agents opportunistically discover available context via `context_manager.get()` and build intelligent prompts that include whatever context exists. LLMs interpret relevance and synthesize information through template-driven instructions.

### Intelligence Distribution ✅ DECIDED

**Question**: Where should intelligence reside - in code logic, configuration systems, or LLM execution?

**Decision**: **LLM-Driven Intelligence via Templates**

**Rationale**:
- **Templates as Control Surface**: Users control intelligence through template modification (direct impact)
- **LLM Interpretation**: Models handle context synthesis, gap filling, and relevance determination
- **Emergent Intelligence**: System gets smarter as more agents contribute context
- **Zero Configuration Burden**: Intelligence emerges from template design, not config complexity
- **User Empowerment**: Template editing provides immediate feedback and control
- **Architectural Elegance**: Shifts complexity from configuration to where users have direct control

**Implementation**: Agents become thin wrappers around intelligent template execution. Templates contain instructions for LLMs on how to interpret available context, synthesize information, and produce domain-specific analysis.

### Agent Collaboration Model ✅ DECIDED

**Question**: Should agents be context-dependent (requiring specific inputs) or context-aware (adapting to available information)?

**Decision**: **Context-Aware Agents with Opportunistic Enhancement**

**Rationale**:
- **Plug-and-Play Experience**: Agents work standalone or with any available context
- **Progressive Enhancement**: More context improves quality, but agents remain functional with less
- **Future-Proof**: New agents automatically enhance existing agents without configuration changes
- **LLM-Driven Adaptation**: Models determine how to best use available context
- **Zero Dependencies**: No agent requires specific inputs from other agents
- **Emergent Collaboration**: Agents naturally benefit from each other's contributions

**Implementation**: Each agent scavenges available context via opportunistic discovery, builds intelligent prompts that adapt to context availability, and produces valuable output regardless of context richness.

### Cache Granularity ✅ DECIDED

**Question**: Should caching happen at the agent level or orchestrator level?

**Decision**: **Agent-Level Caching**

**Rationale**:
- Aligns with app philosophy of complete flexibility
- Orchestrator focuses on its main task - orchestrating
- More granular cache invalidation saves costs on expensive LLM calls
- Individual agents can implement domain-specific caching strategies
- Better performance optimization at the agent level
- Supports stateless agent design while maintaining efficiency

### Agent Configuration ✅ DECIDED

**Question**: Should agents have their own configuration sections, or consume shared project config?

**Decision**: **Agent-Specific Configuration Sections with Sensible Defaults**

**Rationale**:
- Maximum developer choice: Different agents can use optimal LLM providers for their tasks
- Progressive enhancement: Shared defaults with agent-specific overrides
- Future-proofing: New agents can add specialized configuration needs
- Cost optimization: Teams can use expensive models where they add most value
- Developer experience: Power users get full control, beginners get sensible defaults
- Aligns perfectly with philosophy of complete flexibility and meeting developers where they are

### Error Boundaries ✅ DECIDED

**Question**: When an agent fails, should the pipeline halt, continue with fallbacks, or allow manual intervention?

**Decision**: **Hybrid Approach with Configuration**

**Rationale**:
- Configurable failure behavior per agent allows maximum flexibility
- Developers can specify retry counts, fallback strategies, and timeout settings
- Agents can be marked as "required" vs "optional" 
- Supports various fallback strategies: use cache, use defaults, skip agent, halt pipeline
- Maintains automation benefits while giving developers control
- Fits perfectly with "meet developers where they are" philosophy

### LLM Provider Per Agent ✅ DECIDED

**Question**: Should different agents be able to use different LLM providers?

**Decision**: **Different LLM Providers Per Agent**

**Rationale**:
- Maximum flexibility: Users configure providers wherever they feel necessary
- Cost burden shifted to users: They decide when/where to use expensive models
- Leverage model-specific strengths for optimal results
- Supports teams with different provider access/preferences
- Future enterprise feature opportunity: Automatic cost reduction measures
- Aligns with "meet developers where they are" philosophy
- Enables provider diversification and resilience strategies

---

## System Components

### Core Managers

#### ConfigManager
**Responsibilities**: 
- Load and validate project configuration with agent-specific sections
- Handle configuration inheritance (defaults → agent overrides)
- Provide agent execution ordering
- Support configurable template directories

**Key Methods**:
- `get_agent_config(agent_name: str) -> Dict`
- `get_agent_execution_order() -> List[str]`
- `get(key: str, default: Any = None) -> Any`

#### LLMManager
**Responsibilities**:
- Abstract LLM provider execution across different providers
- Handle cross-platform command execution  
- Support per-agent provider configuration
- Implement retry logic and error handling

**Key Methods**:
- `execute(prompt: str, agent_name: str) -> str`
- `validate_provider(provider: str) -> bool`
- `get_available_providers() -> Dict[str, bool]`

#### ContextManager
**Responsibilities**:
- Manage shared context pool for opportunistic discovery
- Support context accumulation without rigid structure
- Provide simple get/set interface for agent use
- Enable context-based caching strategies

**Key Methods**:
- `get(key: str, default: Any = None) -> Any`
- `set(key: str, value: Any) -> None`
- `add(key: str, value: Any) -> None`
- `keys() -> List[str]`

#### Agent Orchestrator
**Responsibilities**:
- Execute agents in configured order
- Inject managers into agent instances
- Handle pipeline-level error recovery
- Provide execution progress feedback

**Key Methods**:
- `run_sequence(feature_request: str) -> str`
- `load_agents() -> None`
- `get_execution_sequence() -> List[BaseAgent]`

---

## Agent Architecture

### Agent Design Pattern
All agents follow this consistent pattern:

```python
def execute(self, feature_request: str) -> str:
    # 1. Opportunistic context discovery
    available_context = self._discover_available_context()
    
    # 2. Template-driven prompt building
    prompt = self._build_intelligent_prompt(feature_request, available_context)
    
    # 3. LLM execution with agent-specific provider
    result = self.llm_manager.execute(prompt, agent_name="agent_name")
    
    # 4. Context contribution for other agents
    self.context_manager.set("agent_output_key", result)
    
    return result

def _discover_available_context(self) -> Dict[str, Any]:
    """Opportunistically gather any useful context."""
    return {
        'project_analysis': self.context_manager.get("project_analysis_summary"),
        'project_structure': self.context_manager.get("project_structure"),  
        'research_findings': self.context_manager.get("feature_research_summary"),
        # Agent decides what context might be useful
    }
```

### MVP Agent Implementations

#### 1. ProjectAnalysisAgent
- **Task**: Analyze codebase structure, patterns, and conventions
- **Context Discovery**: None (first agent in pipeline)
- **Context Contribution**: `project_analysis_summary`, `project_structure`, `tech_stack_info`
- **Template Focus**: Codebase pattern extraction and architectural analysis
- **LLM Strategy**: Use analytical models (Claude) for structured code analysis

#### 2. FeatureResearchAgent  
- **Task**: Research domain best practices and technical approaches
- **Context Discovery**: Project analysis, codebase structure, existing patterns
- **Context Contribution**: `feature_research_summary`, `implementation_strategies`, `best_practices`
- **Template Focus**: Domain research with project-specific context awareness
- **LLM Strategy**: Use creative models (Gemini) for broad research and ideation

#### 3. PromptAssemblyAgent
- **Task**: Synthesize all available context into optimized coding prompt
- **Context Discovery**: All available context from previous agents
- **Context Contribution**: `final_coding_prompt`, `implementation_guidance`
- **Template Focus**: Context synthesis and coding prompt optimization
- **LLM Strategy**: Use precise models (Claude) for structured prompt assembly

---

## Template System

### Template Structure
```
templates/
├── agents/
│   ├── project_analysis_template.md
│   ├── feature_research_template.md
│   └── prompt_assembly_template.md
└── shared/
    ├── context_snippets.md
    └── common_instructions.md
```

### Template Pattern
Templates use LLM-interpretable instructions rather than rigid placeholders:

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

**Context Interpretation Instructions:**
- If project analysis is available, focus research on integration points
- If codebase structure is known, align with existing patterns  
- If no context available, provide general best practices
- Always provide actionable implementation guidance

**Output Requirements:**
[Specific structured output format]
```

---

## Configuration

### Minimal Configuration Approach
```json
{
  "project": {
    "name": "my-project",
    "context": "Brief project description",
    "tech_stack": "Technology stack summary", 
    "architecture": "Architectural overview"
  },
  "agent_execution_order": [
    "project-analysis-agent",
    "feature-research-agent", 
    "prompt-assembly-agent"
  ],
  "llm_settings": {
    "default_provider": "gemini",
    "temperature": 0.7
  },
  "templates": {
    "directories": ["./templates", "./custom-templates"]
  }
}
```

### Agent-Specific Overrides (Optional)
```json
{
  "agents": {
    "project_analysis_agent": {
      "llm": {
        "provider": "claude",
        "temperature": 0.3
      }
    },
    "feature_research_agent": {
      "llm": {
        "provider": "gemini", 
        "temperature": 0.8
      }
    }
  }
}
```

---

## System Workflow

1. **User Input**: Feature request provided via CLI
2. **Configuration Loading**: ConfigManager loads project config and agent settings
3. **Agent Orchestration**: Agents executed in configured order
4. **Context Discovery**: Each agent scavenges available context
5. **Template Execution**: LLMs interpret context and generate analysis
6. **Context Contribution**: Agent results stored for subsequent agents
7. **Progressive Enhancement**: Later agents benefit from richer context
8. **Final Output**: Optimized coding prompt ready for implementation

---

## Benefits of This Architecture

### For Users
- **Zero Configuration Overhead**: Add agents without configuration changes
- **Template Control**: Direct control over intelligence through template editing
- **Progressive Enhancement**: System improves automatically as agents are added
- **Plug-and-Play**: Agents work in any combination or order

### For Developers  
- **Simple Agent Development**: Follow established pattern for new agents
- **No Rigid Dependencies**: Agents remain functional regardless of execution context
- **Template-Driven Intelligence**: Focus on prompt engineering rather than complex logic
- **Emergent Collaboration**: Agents naturally enhance each other's capabilities

### For System Evolution
- **Future-Proof**: New agents automatically enhance existing agents
- **Scalable Intelligence**: More agents = richer context for all agents
- **Maintainable**: Intelligence lives in templates, not scattered code logic
- **Extensible**: Community can contribute agents and templates independently

---

## Success Metrics

### Technical Success
- 3-agent pipeline completes successfully 
- Users can configure different providers per agent
- Final prompts are structured and complete

### User Value Success  
- Final coding prompts produce better code than monolithic approach
- Users report value from provider choice flexibility
- Setup takes <10 minutes for new projects

### Architectural Success
- New agents can be added without configuration changes
- Template modifications provide immediate intelligence control
- System demonstrates emergent collaboration between agents