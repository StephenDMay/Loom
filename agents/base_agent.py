from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING

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

    def _log_error(self, message: str):
        """
        Log error messages. Override this method to customize logging behavior.
        
        Args:
            message (str): The error message to log.
        """
        print(f"ERROR [{self.__class__.__name__}]: {message}")

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
