# agent.py

class ExampleAgent:
    """
    This is a simple example of an agent.
    It has a 'run' method that takes a task description and returns a message.
    """
    def run(self, task_description: str) -> str:
        """
        Executes the agent's task.

        Args:
            task_description: A string describing the task to be performed.

        Returns:
            A string confirming the task was received.
        """
        return f"ExampleAgent received: {task_description}"
