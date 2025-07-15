from agents.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    """
    This is a simple example of an agent that inherits from BaseAgent.
    """
    def execute(self, task_description: str, *args, **kwargs) -> str:
        """
        Executes the agent's task by taking a task description.

        Args:
            task_description: A string describing the task to be performed.

        Returns:
            A string confirming the task was received.
        """
        return f"ExampleAgent received: {task_description}"
