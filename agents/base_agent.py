from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    """

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
