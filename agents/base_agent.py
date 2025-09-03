from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from core.llm_manager import LLMManager
    from core.context_manager import ContextManager

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """

    def __init__(self, config: Optional[Dict] = None, llm_manager: Optional['LLMManager'] = None, context_manager: Optional['ContextManager'] = None):
        """
        Initializes the agent with an optional configuration dictionary, LLM manager, and context manager.

        Args:
            config (Optional[Dict]): Configuration for the agent.
            llm_manager (Optional[LLMManager]): LLM manager instance for making LLM calls.
            context_manager (Optional[ContextManager]): Context manager instance for sharing state between agents.
        """
        self.config = config or {}
        self.llm_manager = llm_manager
        self.context_manager = context_manager
        
        # Set up agent-specific logger
        self.logger = logging.getLogger(f"agents.{self.__class__.__name__}")
        
        # Configure agent-specific log level if specified
        agent_log_level = self.config.get('log_level')
        if agent_log_level:
            try:
                self.logger.setLevel(getattr(logging, agent_log_level.upper()))
            except (AttributeError, ValueError):
                pass  # Fall back to global log level

    def log(self, message: str, level: str = "info"):
        """
        Log messages with the specified level.
        
        Args:
            message (str): The message to log.
            level (str): The log level (debug, info, warning, error, critical).
        """
        try:
            log_level = getattr(logging, level.upper())
            self.logger.log(log_level, message)
        except AttributeError:
            # Fallback to info level for invalid log levels
            self.logger.info(f"[INVALID_LEVEL:{level}] {message}")

    def _log_error(self, message: str):
        """
        Log error messages. Uses the new log method for consistency.
        
        Args:
            message (str): The error message to log.
        """
        self.log(message, "error")

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the agent's primary task.

        This method should be overridden by all concrete agent implementations.
        The flexible signature (*args, **kwargs) allows for diverse agent
        needs, but it is the responsibility of the orchestrator to provide
        the correct arguments.

        Returns:
            Any: The result of the agent's execution.
        """
        pass
