# Universal Development Issue Generator

A meta-prompt system that automates feature research and GitHub issue creation for any software project. Inspired by the "prompt that builds other prompts" concept for streamlining development workflow planning.

## 🎯 What It Does

Transforms this:
```bash
python dev-issue.py "implement real-time tournament bracket tracking"
```

Into this:
- Comprehensive feature research document
- Technical implementation specification  
- Risk assessment and mitigation strategies
- Ready-to-use GitHub issue with acceptance criteria
- Effort estimates and dependency analysis

## 🚀 Quick Start

### 1. Installation
```bash
# Clone or download the generator
git clone [repository-url] ~/.dev-issue-generator
cd ~/.dev-issue-generator

# Ensure Python 3.7+ is installed
python --version

# No additional Python packages required - uses only standard library
```

### 2. Configuration
```bash
# Navigate to your project directory
cd /path/to/your/project

# Interactive setup for your project
python ~/.dev-issue-generator/dev-issue.py init
```

### 3. Generate Your First Issue
```bash
# Basic usage
python ~/.dev-issue-generator/dev-issue.py "implement user authentication system"

# Template-specific shortcuts
python ~/.dev-issue-generator/dev-issue.py --template data "optimize Limitless API sync pipeline"
python ~/.dev-issue-generator/dev-issue.py --template ui "improve dashboard performance metrics"
python ~/.dev-issue-generator/dev-issue.py --template api "add tournament bracket endpoints"
python ~/.dev-issue-generator/dev-issue.py --template perf "implement Redis caching layer"
```

### 4. Optional: Create Global Command
**Windows:**
Create `dev-issue.bat` in a directory in your PATH:
```batch
@echo off
python "C:\path\to\.dev-issue-generator\dev-issue.py" %*
```

**Mac/Linux:**
Create a symlink or alias:
```bash
# Symlink approach
ln -s ~/.dev-issue-generator/dev-issue.py /usr/local/bin/dev-issue

# Or add alias to your shell profile
echo 'alias dev-issue="python ~/.dev-issue-generator/dev-issue.py"' >> ~/.bashrc
```

## 📁 Project Structure

```
~/.dev-issue-generator/
├── dev-issue.py                    # Main Python script
├── meta-prompt-template.md         # Universal meta-prompt template
└── README.md                       # This file

# Per-project files (created in your project directory):
your-project/
├── dev-automation.config.json      # Project configuration
└── generated-issues/               # Output directory
    ├── 20240714_123456_feature.md  # Generated specifications
    └── ...
```

## 🛠️ Configuration

Each project gets its own `dev-automation.config.json` file created by running `python dev-issue.py init`.

### Project Settings
```json
{
  "project": {
    "name": "Your Project Name",
    "context": "What your project does and its domain",
    "tech_stack": "Technologies, frameworks, languages used",
    "architecture": "High-level architectural pattern",
    "target_users": "Primary user base and characteristics",
    "constraints": "Technical, business, regulatory constraints"
  }
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

### Basic Feature Generation
```bash
# Generate comprehensive research for any feature
python dev-issue.py "implement OAuth2 authentication"
python dev-issue.py "add real-time notifications"
python dev-issue.py "optimize database query performance"
```

### Template-Specific Generation
```bash
# UI/UX features
python dev-issue.py --template ui "redesign user dashboard with accessibility improvements"

# Backend/API features  
python dev-issue.py --template api "implement rate limiting with Redis"

# Data pipeline features
python dev-issue.py --template data "build ETL pipeline for external API integration"

# Performance optimization
python dev-issue.py --template perf "optimize React bundle size and loading speed"
```

### Advanced Usage
```bash
# Override LLM provider
python dev-issue.py --provider claude-code "implement microservices architecture"

# Use custom config file
python dev-issue.py --config ./enterprise-project.json "add SAML SSO integration"

# Dry run (generate prompt without executing LLM)
python dev-issue.py --dry-run "implement blockchain integration"
```

## 🔧 GitHub Integration

### Automatic Issue Creation
When `auto_create_issues` is enabled in your config:
```bash
# This will automatically create a GitHub issue with full specification
python dev-issue.py "implement user roles and permissions"
```

### Manual Issue Creation
```bash
# Generate specification file
python dev-issue.py "implement user roles and permissions"

# Use the generated file with GitHub CLI
gh issue create --body-file generated-issues/[timestamp]_feature.md --label "enhancement"
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
python ~/.dev-issue-generator/dev-issue.py init  # Creates config for this project
python ~/.dev-issue-generator/dev-issue.py "add user authentication"

# Project B  
cd ~/projects/my-mobile-app
python ~/.dev-issue-generator/dev-issue.py init  # Creates different config for this project
python ~/.dev-issue-generator/dev-issue.py "implement offline sync"

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

**🎯 The Goal**: Transform feature ideas into well-researched, actionable development tasks in minutes instead of hours. Fix problems at the planning stage through comprehensive upfront research and technical specification.