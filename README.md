# Universal Development Issue Generator

A meta-prompt system that automates feature research and GitHub issue creation for any software project. Inspired by the "prompt that builds other prompts" concept for streamlining development workflow planning.

## 🎯 What It Does

Transforms this:
```bash
dev-issue "implement real-time tournament bracket tracking"
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
# Download and run setup script
curl -sSL [setup-script-url] | bash

# Or manual setup:
mkdir ~/.dev-issue-generator && cd ~/.dev-issue-generator
# Copy artifacts: meta-prompt-template.md, dev-issue, setup files
chmod +x dev-issue
```

### 2. Configuration
```bash
# Interactive setup for your project
./dev-issue init

# Or copy the Pokemon TCG sample config and modify
cp dev-automation.config.json my-project.config.json
```

### 3. Generate Your First Issue
```bash
# Basic usage
./dev-issue "implement user authentication system"

# Template-specific shortcuts
./tcg-data "optimize Limitless API sync pipeline"
./tcg-ui "improve dashboard performance metrics"
./tcg-api "add tournament bracket endpoints"
./tcg-perf "implement Redis caching layer"
```

## 📁 Project Structure

```
~/.dev-issue-generator/
├── dev-issue                      # Main CLI script
├── meta-prompt-template.md         # Universal meta-prompt
├── dev-automation.config.json      # Project configuration
├── generated-issues/               # Output directory
├── github-integration.sh           # GitHub issue creation helper
└── tcg-* scripts                   # Template shortcuts
```

## 🛠️ Configuration

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
    "research_depth": "comprehensive" # brief, standard, comprehensive
  }
}
```

### Template Customization
```json
{
  "templates": {
    "ui_feature": "Focus on user experience, responsive design...",
    "api_feature": "Focus on performance, security, scalability...",
    "data_pipeline": "Focus on data processing, ETL, validation..."
  }
}
```

## 🎪 Usage Examples

### Basic Feature Generation
```bash
# Generate comprehensive research for any feature
./dev-issue "implement OAuth2 authentication"
./dev-issue "add real-time notifications"
./dev-issue "optimize database query performance"
```

### Template-Specific Generation
```bash
# UI/UX features
./dev-issue ui "redesign user dashboard with accessibility improvements"

# Backend/API features  
./dev-issue api "implement rate limiting with Redis"

# Data pipeline features
./dev-issue data "build ETL pipeline for external API integration"

# Performance optimization
./dev-issue perf "optimize React bundle size and loading speed"
```

### Pokemon TCG App Examples
```bash
# Tournament data features
./tcg-data "implement incremental sync for Limitless API tournament results"

# Meta analysis features
./tcg-ui "build interactive matchup matrix with win rate visualization"

# Performance features
./tcg-perf "optimize meta snapshot calculations for real-time updates"

# API features
./tcg-api "add deck recommendation endpoints with personalization"
```

### Advanced Usage
```bash
# Override LLM provider
LLM_PROVIDER=claude-code ./dev-issue "implement microservices architecture"

# Use custom config
CONFIG_FILE=./enterprise-project.json ./dev-issue "add SAML SSO integration"

# Dry run (generate prompt without executing)
./dev-issue --dry-run "implement blockchain integration"
```

## 🔧 GitHub Integration

### Manual Issue Creation
```bash
# Generate issue specification
./dev-issue "implement user roles and permissions" > issue.md

# Create GitHub issue
gh issue create --body-file issue.md --label "enhancement,auto-generated"
```

### Automated Integration (Future)
```bash
# Direct issue creation (when auto_create_issues: true)
./dev-issue "add two-factor authentication"
# → Automatically creates GitHub issue with research and specifications
```

## 🎨 Customization

### Adding New Templates
```json
{
  "templates": {
    "security": "Focus on authentication, authorization, data protection...",
    "mobile": "Focus on responsive design, touch interfaces, offline support...",
    "devops": "Focus on CI/CD, deployment automation, monitoring..."
  }
}
```

### Creating Custom Commands
```bash
#!/bin/bash
# my-security (custom security feature generator)
./dev-issue security "$*"
```

### Multi-Project Management
```bash
# Different configs for different projects
alias tcg-issue="CONFIG_FILE=./tcg-project.json ./dev-issue"
alias ecom-issue="CONFIG_FILE=./ecommerce-project.json ./dev-issue"
alias blog-issue="CONFIG_FILE=./blog-project.json ./dev-issue"
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
- `jq` - JSON processor for configuration parsing
- LLM CLI tool (one of):
  - `gemini-cli` for Google Gemini
  - `claude-code` for Anthropic Claude  
  - `openai` for OpenAI GPT

### Optional
- `gh` - GitHub CLI for automated issue creation
- `git` - For repository context and integration

## 🚧 Roadmap

- [ ] **GitHub Actions Integration** - Trigger issue generation from repository events
- [ ] **Template Marketplace** - Share and discover project templates
- [ ] **Multi-LLM Comparison** - Generate issues with multiple providers
- [ ] **Progress Tracking** - Monitor implementation progress and outcomes
- [ ] **Team Collaboration** - Shared configurations and team workflows
- [ ] **IDE Integration** - VSCode extension for in-editor issue generation

## 🤝 Contributing

This is a universal system designed to work across any project type. Contributions welcome for:

- New template categories
- LLM provider integrations  
- Output format improvements
- GitHub workflow automation
- Documentation and examples

## 📄 License

MIT License - Use this system for any project, commercial or personal.

---

**🎯 The Goal**: Fix problems at the lowest value stage through better upfront research and planning. Turn feature ideas into well-researched, actionable development tasks in minutes instead of hours.