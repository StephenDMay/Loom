# Auto-Dev Multi-Agent Architecture Documentation

## System Overview

Auto-dev is a multi-agent system that transforms feature requests into comprehensive coding prompts through sequential agent analysis. The system uses LLM-driven template population to offload analysis, interpretation, and compilation to language models at each step.

## Core Architecture Decisions

### Context Passing Strategy ✅ DECIDED
**Decision**: Full Context Objects
- **Rationale**: Cross-pollination benefits between agents, quality improvement through comprehensive understanding, debugging transparency
- **Implementation**: Each agent receives complete context and adds their analysis to shared context object
- **Trade-offs**: Larger context size vs. better agent coordination and flexibility

### Cache Granularity ✅ DECIDED
**Decision**: Agent-Level Caching
- **Rationale**: Aligns with complete flexibility philosophy, granular cache invalidation saves LLM costs, better performance optimization
- **Implementation**: Each agent manages its own cache using context hashing for keys
- **Trade-offs**: More complexity vs. cost optimization and flexibility

### Agent Configuration ✅ DECIDED
**Decision**: Agent-Specific Configuration Sections
- **Rationale**: Maximum developer choice, progressive enhancement with defaults, future-proofing, cost optimization
- **Implementation**: Shared defaults with agent-specific overrides in config file
- **Trade-offs**: Configuration complexity vs. complete flexibility

### Error Boundaries ✅ DECIDED
**Decision**: Hybrid Approach with Configuration
- **Rationale**: Configurable failure behavior per agent, supports various fallback strategies, maintains automation with developer control
- **Implementation**: Per-agent error handling configuration with retry counts, fallback strategies, and timeout settings
- **Trade-offs**: Configuration complexity vs. maximum flexibility

### LLM Provider Per Agent ✅ DECIDED
**Decision**: Different LLM Providers Per Agent
- **Rationale**: Cost optimization, leverage model-specific strengths, supports diverse team preferences, enables resilience strategies
- **Implementation**: Per-agent LLM provider configuration with fallback to defaults
- **Trade-offs**: Testing complexity vs. optimal model utilization

### Template Strategy ✅ DECIDED
**Decision**: Placeholder-Based with LLM Interpretation
- **Rationale**: User structural control with flexible LLM interpretation, human-in-the-loop review for MVP validation
- **Implementation**: Per-agent templates + golden template with simple placeholders like `{{PROJECT_ANALYSIS}}`
- **Trade-offs**: Prompt engineering requirements vs. implementation simplicity

### Agent Sequencing ✅ DECIDED
**Decision**: Configurable Order with Defaults
- **Rationale**: User control over pipeline execution, sensible defaults for common workflows
- **Implementation**: Order field in agent configuration, fallback to discovery order
- **Trade-offs**: Configuration overhead vs. workflow flexibility

### File Management Strategy ✅ DECIDED
**Decision**: Memory-Based Handoff for MVP
- **Rationale**: Simpler implementation, faster execution, easier debugging, natural fit for sequential workflow
- **Implementation**: Context object passed between agents, only final golden prompt written to file
- **Trade-offs**: No intermediate inspection vs. simplicity

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
- `get_template_directory() -> Path`
- `get_project_config() -> Dict`

#### LLMManager
**Responsibilities**:
- Abstract LLM provider execution across different providers
- Handle cross-platform command execution
- Support per-agent provider configuration
- Implement retry logic and error handling

**Key Methods**:
- `execute_for_agent(agent_name: str, prompt: str) -> str`
- `validate_provider(provider: str) -> bool`
- `_execute_with_retry(provider: str, prompt: str, retry_count: int) -> str`

#### ContextManager
**Responsibilities**:
- Manage context objects between agents
- Support sequential context accumulation
- Handle context hashing for cache keys
- Provide context serialization for caching

**Key Methods**:
- `create_context(feature_request: str, project_config: Dict) -> Dict`
- `add_agent_output(context: Dict, agent_name: str, output: str) -> Dict`
- `get_context_hash(context: Dict) -> str`

#### FileManager
**Responsibilities**:
- Handle template loading with configurable paths
- Support template resolution hierarchy
- Manage output file creation
- Maintain existing file naming conventions

**Key Methods**:
- `load_agent_template(agent_name: str) -> str`
- `load_golden_template() -> str`
- `write_final_prompt(content: str, feature_name: str, timestamp: str) -> Path`

### Agent Architecture

#### Priority 1: MVP Agents
1. **ProjectAnalysisAgent**
   - **Task**: Analyze codebase structure, patterns, and conventions
   - **Input**: Feature request + project config + codebase scan
   - **Output**: Project analysis with file listings, code snippets, interfaces, design decisions

2. **FeatureResearchAgent**
   - **Task**: Research domain best practices and technical approaches
   - **Input**: Feature request + project analysis + context
   - **Output**: Research findings with industry patterns, best practices, implementation strategies

3. **PromptAssemblyAgent**
   - **Task**: Combine all agent outputs into optimized coding prompt
   - **Input**: Feature request + all previous agent outputs + golden template
   - **Output**: Final coding prompt ready for coding LLM

#### Priority 2: Enhancement Agents
4. **DocumentationAgent**
   - **Task**: Generate GitHub issues and project documentation
   - **Input**: Research results + prompts
   - **Output**: GitHub issues, specifications, acceptance criteria

## Configuration Structure

```json
{
  "project": {
    "name": "my-project",
    "type": "web-app"
  },
  "templates": {
    "directory": "./custom-templates"
  },
  "defaults": {
    "llm_provider": "gemini",
    "temperature": 0.7,
    "retry_count": 3
  },
  "agents": {
    "project_analysis": {
      "llm_provider": "claude",
      "temperature": 0.3,
      "order": 1
    },
    "feature_research": {
      "llm_provider": "gemini",
      "temperature": 0.8,
      "order": 2
    },
    "prompt_assembly": {
      "llm_provider": "claude",
      "order": 3
    }
  }
}
```

## Template Structure

```
templates/
├── agents/
│   ├── project_analysis.md
│   ├── feature_research.md
│   └── prompt_assembly.md
└── golden_prompt.md
```

## System Workflow

1. **User Input**: Feature request provided via CLI
2. **Configuration Loading**: ConfigManager loads project config and agent settings
3. **Agent Orchestration**: Agents executed in configured order
4. **Sequential Processing**: Each agent receives growing context, adds analysis
5. **Template Population**: PromptAssemblyAgent uses golden template with placeholders
6. **Human Review**: Generated prompt reviewed before coding LLM execution
7. **Final Output**: Optimized coding prompt ready for implementation

## Philosophy Alignment

- **Complete Flexibility**: Users control templates, agent order, LLM providers, error handling
- **Meet Developers Where They Are**: Sensible defaults with progressive enhancement
- **LLM-Driven Intelligence**: Analysis, interpretation, and compilation handled by LLMs
- **Human-in-the-Loop**: Review points ensure quality and control