# Development Task: Add agent execution visibility

## Feature Implementation Request
Implement a mechanism to add visibility into agent execution within the Loom project. This includes logging key events, inputs, and outputs of agents to aid in debugging, monitoring, and performance analysis.

## Project Context
**Project**: Loom
**Architecture**: Agent-based, Modular, Configuration-driven, Model-agnostic
**Tech Stack**: Python 3.7+, ChatGPT, Claude, Gemini, pip, jsonschema

## Implementation Specifications

### Requirements Analysis
1.  **Base Logging Method:** Add a base logging method to the `BaseAgent` class in `agents/base_agent.py`. This method should accept a message and a log level as input, utilizing Python's built-in `logging` module.
2.  **Orchestrator Logging:** Modify `agents/orchestrator.py` to log agent execution details before and after each agent's `run()` method. Log the agent's name, input, and output.
3.  **Configuration:** Update `core/config_schema.json` to allow users to configure the global log level and potentially agent-specific log levels.
4.  **Configuration Loading:** Modify `core/config_manager.py` to load and apply the log level configuration.
5.  **Asynchronous Logging (Optional):** If performance becomes an issue, implement asynchronous logging using Python's `asyncio` or `threading` modules.
6.  **Logging Decorator (Enhancement):** Implement a decorator (e.g., `@log_execution`) that can be applied to agent's `run()` methods to automatically log execution details.
7.  **Detailed Logging (Enhancement):** Add more detailed logging information, such as execution time, memory usage, and LLM usage (if applicable).
8.  **Monitoring Integration (Future):** Consider integrating with monitoring tools like the ELK stack or Prometheus for advanced log analysis and visualization.

### Technical Constraints
1.  **Performance:** Adding visibility should not significantly impact agent execution time. Consider asynchronous logging or sampling to minimize overhead.
2.  **Security:** Ensure that no sensitive data (API keys, user data) is logged. Implement data masking or redaction techniques if necessary.
3.  **Error Handling:** The visibility feature itself should not introduce new errors or interfere with existing error handling.
4.  **Testability:** Add tests to verify that the visibility feature works as expected and does not negatively impact performance.

### Integration Requirements
1.  **`agents/base_agent.py`:** Add the `log` method to the `BaseAgent` class.
2.  **`agents/orchestrator.py`:** Add logging calls before and after each agent's `run()` method.
3.  **`core/config_schema.json`:** Add configuration options for the log level. Example:

{
  "type": "object",
  "properties": {
    "log_level": {
      "type": "string",
      "enum": ["debug", "info", "warning", "error", "critical"],
      "default": "info",
      "description": "The global log level for the application."
    },
    "agents": {
      "type": "object",
      "description": "Agent specific configurations",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "log_level": {
            "type": "string",
            "enum": ["debug", "info", "warning", "error", "critical"],
            "description": "The log level for the specific agent."
          }
        }
      }
    }
  }
}

4.  **`core/config_manager.py`:** Load and apply the log level configuration. Example:

import logging
import json
from jsonschema import validate, ValidationError

class ConfigManager:
    def __init__(self, config_path="core/config_schema.json"):
        self.config_path = config_path
        self.config = self.load_and_validate_config()
        self.configure_logging()

    def load_and_validate_config(self):
        # Existing config loading logic
        ...
        return config

    def configure_logging(self):
        log_level = self.config.get("log_level", "info").upper()
        logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Configure agent-specific log levels
        agents_config = self.config.get("agents", {})
        for agent_name, agent_config in agents_config.items():
            agent_log_level = agent_config.get("log_level", log_level).upper()
            logger = logging.getLogger(f"agents.{agent_name}")  # Assuming agent loggers are named this way
            try:
                logger.setLevel(agent_log_level)
            except ValueError:
                print(f"Invalid log level '{agent_log_level}' for agent '{agent_name}'. Using default level.")
                logger.setLevel(log_level)

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project. Look for existing logging patterns in `agents/base_agent.py` or `core/llm_manager.py`. The `ProjectAnalysisAgent` in `agents/project_analysis_agent/agent.py` is the largest agent and may contain useful logging examples.
- Implement comprehensive error handling and input validation. Look for `try...except` blocks in `agents/orchestrator.py` and `core/llm_manager.py` as examples.
- Write unit tests for all new functionality.
- Document public APIs and complex business logic.
- Consider performance implications and optimization opportunities.

### Security Considerations
- Implement proper authentication and authorization checks (though not directly relevant to this feature, any logging should avoid exposing sensitive data).
- Sanitize and validate all user inputs.
- Follow secure coding practices for the technology stack.
- Consider data privacy and compliance requirements.

### Implementation Approach
1. **Analysis Phase**: Review existing codebase patterns and similar implementations.
2. **Design Phase**: Plan the architecture and identify integration points.
3. **Development Phase**: Implement following established patterns and conventions.
4. **Testing Phase**: Write and run comprehensive tests.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [x] Modified `agents/base_agent.py` with a base logging method.
- [x] Modified `agents/orchestrator.py` to log agent execution details.
- [x] Updated `core/config_schema.json` with log level configuration options.
- [x] Modified `core/config_manager.py` to load and apply the log level configuration.
- [ ] Unit tests achieving minimum 80% code coverage for the new logging functionality.
- [ ] Integration tests for the interaction between agents and the logging system.

### Documentation Updates
- [ ] API documentation for new functions (if any).
- [ ] README updates if user-facing features are added.
- [ ] Architecture documentation updates if patterns change.
- [ ] Deployment or setup instruction updates if required.

### Quality Assurance
- [ ] Code passes all existing tests.
- [ ] New functionality is properly tested.
- [ ] Code follows project style guidelines.
- [ ] Performance benchmarks are within acceptable ranges.
- [ ] Security review completed for sensitive operations.

## Success Criteria
1.  Agent execution details (name, input, output) are logged correctly at the configured log level.
2.  The log level can be configured globally and potentially for individual agents via `core/config_schema.json` and `core/config_manager.py`.
3.  The logging implementation does not significantly impact agent execution time.
4.  No sensitive data is logged.
5.  Unit and integration tests cover the new logging functionality.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code. Start with Phase 1 (Basic Logging Implementation) and then proceed to Phase 2 (Enhanced Logging and Configuration) if time permits. Phase 3 (Monitoring Integration) is a future consideration.