from agents.base_agent import BaseAgent
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.llm_manager import LLMManager

class ExampleAgent(BaseAgent):
    """
    This is a simple example of an agent that inherits from BaseAgent.
    """
    def __init__(self, config: Optional[Dict] = None, llm_manager: Optional['LLMManager'] = None):
        super().__init__(config, llm_manager)

    def execute(self, task_description: str, *args, **kwargs) -> str:
        """
        Executes the agent's task by taking a task description.

        Args:
            task_description: A string describing the task to be performed.

        Returns:
            A string confirming the task was received.
        """
        return f"ExampleAgent received: {task_description}"
