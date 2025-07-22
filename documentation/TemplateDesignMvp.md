# MVP Template System Features

## Week 1: Core Template System (MVP Essentials)

### TASK-001: Add basic template loading to ProjectAnalysisAgent
**Effort**: 6-8 hours
- Create `agents/project_analysis_agent/templates/analysis_prompt.md` with the feature-focused content
- Add `_load_template()` method with simple file reading and basic fallback
- Add `_populate_template()` method with string replacement for key placeholders
- **MVP Goal**: Agent can load and use a template instead of hardcoded prompts

### TASK-002: Pass feature request to ProjectAnalysisAgent
**Effort**: 3-4 hours
- Update agent's `execute()` method to accept `feature_request` parameter
- Add `{{ feature_request }}` placeholder to template processing
- Update orchestrator to pass initial input to first agent
- **MVP Goal**: Template gets populated with actual feature request

### TASK-003: Create minimal FeatureResearchAgent template
**Effort**: 4-5 hours
- Create basic template that references project analysis output
- Implement same template loading pattern as ProjectAnalysisAgent
- Focus on using `{{ project_analysis_summary }}` from context
- **MVP Goal**: Second agent uses templates and previous agent output

### TASK-004: Create minimal PromptAssemblyAgent template
**Effort**: 4-5 hours
- Create template that combines all previous outputs into final coding prompt
- Use placeholders for all previous agent outputs
- Focus on generating usable coding prompt, not perfect prompt
- **MVP Goal**: Final agent produces template-driven coding prompt

## Week 2: Integration & Basic Polish

### TASK-005: Test and fix 3-agent template pipeline
**Effort**: 6-8 hours
- Run end-to-end tests with real feature requests
- Fix any context passing issues between templated agents
- Ensure final output is actually usable as a coding prompt
- **MVP Goal**: Complete pipeline works with templates start to finish

### TASK-006: Add basic error handling for missing templates
**Effort**: 2-3 hours
- Graceful fallback when template files don't exist
- Simple error messages for template loading failures
- Don't break pipeline execution for template issues
- **MVP Goal**: System doesn't crash when templates are missing

### TASK-007: Basic CLI feedback for template usage
**Effort**: 2-3 hours
- Show which agent is using which template (if any)
- Simple progress indicators for template loading
- Basic error reporting for template problems
- **MVP Goal**: User can see what's happening with templates

## MVP Success Criteria

After these 7 tasks (roughly 2 weeks), you should have:

- ✅ **3-agent pipeline using templates instead of hardcoded prompts**
- ✅ **Feature requests flow through templates to influence analysis**
- ✅ **Each agent builds on previous agent's templated output**
- ✅ **Final output is a usable coding prompt**
- ✅ **System gracefully handles missing templates**
- ✅ **Basic user feedback about template processing**

## What's Explicitly NOT in MVP

- ❌ Template customization or overrides
- ❌ Template validation or quality checking  
- ❌ Performance optimization or caching
- ❌ Advanced error recovery
- ❌ Template versioning
- ❌ Configuration for template directories
- ❌ Template sharing or marketplace features
- ❌ Comprehensive testing beyond basic functionality

## Post-MVP Validation

After completing these tasks, you can:

1. **Test with real feature requests** to see if template-driven output is better than current approach
2. **Compare final prompts** between template vs. non-template approaches
3. **Validate that context flows properly** between templated agents
4. **Identify which template improvements** would have highest impact

**Goal**: Proving the template concept works, not building a production-ready template system.