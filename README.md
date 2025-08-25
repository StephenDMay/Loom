# Loom: The Universal Development Agent Platform

Loom weaves feature requests into comprehensive coding prompts through LLM-driven sequential analysis. Named after the art of weaving disparate threads into cohesive fabric, Loom transforms raw ideas into structured, actionable development plans.

Designed for developers who want to automate the software development lifecycle while retaining complete control over the AI models used at every stage. The core philosophy is **"Meet Developers Where They Are"** - Loom is model-agnostic, allowing you to use any AI model or tool at any step of the process.

## 🎯 What It Does

Loom orchestrates a sequence of specialized AI agents to perform a series of tasks, starting with a simple feature request.

**Example Workflow:**
1. **You provide a task**: `python loom.py "implement real-time tournament bracket tracking"`
2. **Project Analysis Agent**: Scans your codebase to understand existing patterns, tech stack, and conventions.
3. **Feature Research Agent**: Uses the project context to research the best technical approaches and implementation strategies for the feature.
4. **Prompt Assembly Agent**: Synthesizes all the gathered information into a detailed, context-aware coding prompt, ready for an implementation LLM.

The final output is a high-quality, actionable prompt that you can feed into your coding LLM of choice to get consistent and contextually-aware code.

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone [repository-url] ~/Loom
cd ~/Loom

# Ensure Python 3.7+ is installed
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Navigate to your project directory
cd /path/to/your/project

# Copy and configure the project settings
cp ~/Loom/dev-automation.config.json .
# Edit dev-automation.config.json with your project details

# Copy and configure the default template
cp ~/Loom/meta-prompt-template.md .
# Edit meta template to meet your project details, this is the default template used if specific ones are not provided at each step.
```

### 3. Run Your First Agent Sequence
```bash
# Basic usage - runs the configured agent sequence
python ~/Loom/loom.py "implement user authentication system"

# Validate your configuration
python ~/Loom/loom.py --validate-config
```

### 4. Optional: Create Global Command
**Windows:**
Create `loom.bat` in a directory in your PATH:
```batch
@echo off
python "C:\path\to\Loom\loom.py" %*
```

**Mac/Linux:**
Create a symlink or alias:
```bash
# Symlink approach
ln -s ~/Loom/loom.py /usr/local/bin/loom

# Or add alias to your shell profile
echo 'alias loom="python ~/Loom/loom.py"' >> ~/.bashrc
```

## 📁 Project Structure

```
~/Loom/
├── loom.py                         # Main entry point
├── agents/                         # Agent directory
│   ├── orchestrator.py             # Agent orchestration engine
│   ├── base_agent.py               # Base class for all agents
│   ├── project_analysis_agent/     # Analyzes codebase structure
│   ├── feature_research_agent/     # Researches implementation approaches
│   ├── prompt_assembly_agent/      # Assembles final coding prompts
│   └── issue_generator/             # Legacy issue generation
├── core/                           # Core system components
│   ├── config_manager.py           # Configuration management
│   ├── llm_manager.py              # LLM provider abstraction
│   └── context_manager.py          # Cross-agent context sharing
├── requirements.txt                # Python dependencies
└── README.md                       # This file

# Per-project files (created in your project directory):
your-project/
├── dev-automation.config.json      # Project configuration
└── generated-issues/               # Output directory
    ├── 20240714_123456_feature.md  # Generated specifications
    └── ...
```

## 🛠️ Configuration

Each project gets its own `dev-automation.config.json` file that configures the agent execution sequence and LLM providers.

### Project Settings
```json
{
  "project": {
    "name": "Loom",
    "context": "A flexible system that automates the software development lifecycle",
    "tech_stack": "Python, markdown",
    "architecture": "Open orchestration",
    "target_users": "Developers",
    "constraints": "Model API Differences, Context Management, Output Consistency"
  },
  "agent_execution_order": [
    "project-analysis-agent",
    "feature-research-agent", 
    "prompt-assembly-agent"
  ]
}
```

### LLM Provider Settings
```json
{
  "llm_settings": {
    "default_provider": "gemini",     # gemini, claude-code, openai
    "output_format": "structured",    # structured, conversational, json
    "research_depth": "standard",     # brief, standard, comprehensive
    "temperature": 0.7
  }
}
```

### GitHub Integration
```json
{
  "github": {
    "repo_owner": "your-username",
    "repo_name": "your-repo",
    "default_project": "Your-Project-Board-Name",
    "default_labels": ["auto-generated", "needs-review", "enhancement"]
  },
  "automation": {
    "auto_create_issues": true,       # Enable automatic GitHub issue creation
    "auto_assign": false
  }
}
```

### Template Customization
```json
{
  "templates": {
    "ui_feature": "Focus on user experience, responsive design...",
    "api_feature": "Focus on performance, security, scalability...",
    "data_feature": "Focus on data processing, ETL, validation...",
    "perf_feature": "Focus on optimization, caching, performance..."
  }
}
```

## 🎪 Usage Examples

### Basic Agent Execution
```bash
# Run the configured agent sequence
python loom.py "implement OAuth2 authentication"
python loom.py "add real-time notifications"
python loom.py "optimize database query performance"
```

### Configuration Validation
```bash
# Validate your LLM providers and configuration
python loom.py --validate-config
```

## 🤖 Agent System

Loom's power comes from its orchestrated multi-agent architecture. Each agent specializes in a specific aspect of the development workflow:

### Agent Types

**Project Analysis Agent**: Scans your codebase to understand:
- Existing patterns and conventions
- Technology stack and dependencies  
- Architecture and file structure
- Coding standards and practices

**Feature Research Agent**: Conducts comprehensive research on:
- Best practices for the requested feature
- Implementation approaches and alternatives
- Integration considerations with existing codebase
- Potential risks and mitigation strategies

**Prompt Assembly Agent**: Synthesizes information to create:
- Context-aware coding prompts
- Detailed implementation specifications
- Code examples following project conventions
- Ready-to-use prompts for any LLM

### Agent Orchestration

The `AgentOrchestrator` manages the execution sequence:
1. Loads agents dynamically from the `agents/` directory
2. Executes them in the order specified in `agent_execution_order`
3. Manages context sharing between agents via `ContextManager`
4. Handles LLM provider abstraction through `LLMManager`

Agents communicate through a shared context, allowing later agents to build upon the work of earlier ones.

## 🔧 GitHub Integration

### Automatic Issue Creation
When `auto_create_issues` is enabled in your config:
```bash
# This will automatically create a GitHub issue with full specification
python loom.py "implement user roles and permissions"
```

### Manual Issue Creation
```bash
# Generate specification file
python loom.py "implement user roles and permissions"

# Use the generated file with GitHub CLI
gh issue create --body-file generated-issues/YYYY-MM-DD-HHMMSS-feature-slug.md --label "enhancement"
```

### GitHub CLI Setup
```bash
# Install GitHub CLI and authenticate
gh auth login

# Ensure you have project scope for automatic issue creation
gh auth refresh --scopes repo,project
```

## 🎨 Multi-Project Workflow

The beauty of this system is that you can use one installation across multiple projects:

```bash
# Project A
cd ~/projects/my-web-app
cp ~/Loom/dev-automation.config.json .  # Copy and customize config
python ~/Loom/loom.py "add user authentication"

# Project B  
cd ~/projects/my-mobile-app
cp ~/Loom/dev-automation.config.json .  # Copy and customize config
python ~/Loom/loom.py "implement offline sync"

# Each project gets its own config and generated-issues folder
```

## 🔍 Output Format

Each generated issue includes:

- **Executive Summary**: What the feature does and why it matters
- **Codebase Analysis**: Integration points and architectural impact
- **Domain Research**: User workflows and industry best practices
- **Technical Approach**: Implementation strategy with alternatives
- **Implementation Specification**: Detailed technical requirements
- **Risk Assessment**: Technical and business risks with mitigation
- **Project Details**: Effort estimates, dependencies, acceptance criteria
- **GitHub Issue Template**: Ready-to-use issue content

## 🛡️ Dependencies

### Required
- **Python 3.7+**: Uses only standard library (no pip packages needed)
- **LLM CLI tool** (one of):
  - `gemini` (npm package: `npm install -g @google/generative-ai-cli`)
  - `claude-code` for Anthropic Claude  
  - `openai` for OpenAI GPT

### Optional
- **GitHub CLI (`gh`)**: For automated issue creation
- **Git**: For repository context (auto-detected)

### Installation Notes
**Windows**: Ensure Python is in your PATH. NPM-installed tools like `gemini` need the `.cmd` extension but this is handled automatically.

**Mac/Linux**: Standard Python installation should work out of the box.

## 🚧 Roadmap

- [ ] **Multiple LLM Comparison** - Generate issues with multiple providers and compare
- [ ] **Template Marketplace** - Share and discover project-specific templates
- [ ] **Progress Tracking** - Monitor implementation progress and outcomes
- [ ] **Team Collaboration** - Shared configurations and team workflows
- [ ] **IDE Integration** - VSCode extension for in-editor issue generation
- [ ] **CI/CD Integration** - Trigger issue generation from repository events

## 🤝 Contributing

This is a universal system designed to work across any project type. Contributions welcome for:

- New template categories
- LLM provider integrations  
- Output format improvements
- Cross-platform compatibility
- Documentation and examples

## 📄 License

MIT License - Use this system for any project, commercial or personal.

---

**🎯 The Goal**: Weave feature ideas into well-researched, context-aware coding prompts through intelligent agent orchestration. Transform raw concepts into actionable development plans that understand your codebase, follow your patterns, and integrate seamlessly with your workflow.
